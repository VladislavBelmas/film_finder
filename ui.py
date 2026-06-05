from typing import List, Dict, Any, Tuple, Callable
from repositories.movie_repository import MovieRepository


class Menu:
    """Интерактивное меню для поиска фильмов с пагинацией."""

    DESCRIPTION_MAX_LENGTH = 67
    DISPLAY_PAGE_LENGTH = 80

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo
        self.running = True

    def _paginate_result(self, search_func: Callable[..., List[Dict[str, Any]]], search_params: Tuple[Any, ...],
                         current_page: int, limit: int) -> None:
        """Обрабатывает пагинацию результатов поиска."""
        while True:
            films = search_func(*search_params, limit=limit, page=current_page)

            if not films and current_page == 1:
                print("\nРезультатов не найдено.")
                input("\nНажмите Enter для возврата в меню")
                break

            if not films:
                print("\nБольше результатов нет.")
                input("\nНажмите Enter для возврата в меню")
                break

            print(f"\n{'=' * Menu.DISPLAY_PAGE_LENGTH}")
            print(f"СТРАНИЦА {current_page}")
            print(f"{'=' * Menu.DISPLAY_PAGE_LENGTH}")
            self.display_films(films, current_page, limit)

            print(f"\n{'=' * Menu.DISPLAY_PAGE_LENGTH}")
            print("НАВИГАЦИЯ:")
            options = []

            if len(films) == limit:
                options.append("  [N] Следующая страница")

            if current_page > 1:
                options.append("  [P] Предыдущая страница")

            options.append("  [Q] Вернуться в меню")

            for option in options:
                print(option)

            print(f"{'=' * Menu.DISPLAY_PAGE_LENGTH}")

            choice = input("--> Ваш выбор: ").strip().upper()

            if choice == "N":
                if len(films) == limit:
                    current_page += 1
                else:
                    print("\nЭто последняя страница!")
            elif choice == "P":
                if current_page > 1:
                    current_page -= 1
                else:
                    print("\nЭто первая страница!")
            elif choice == "Q" or choice == "":
                break
            else:
                print("\nНеверный выбор!")

    @staticmethod
    def _parse_years_and_pagination(params_str: str, default_min: int, default_max: int,
                                     default_page: int = 1, default_limit: int = 10) -> Tuple[int, int, int, int]:
        try:
            params = params_str.split()
            min_year = int(params[0]) if len(params) >= 1 else default_min
            max_year = int(params[1]) if len(params) >= 2 else default_max
            page = int(params[2]) if len(params) >= 3 else default_page
            limit = int(params[3]) if len(params) >= 4 else default_limit
            return min_year, max_year, page, limit
        except ValueError:
            print("Неверный формат! Используются значения по умолчанию.")
            return default_min, default_max, default_page, default_limit

    @staticmethod
    def _parse_pagination(params_str: str, default_page: int = 1, default_limit: int = 10) -> Tuple[int, int]:
        try:
            params = params_str.split()
            page = int(params[0]) if len(params) >= 1 else default_page
            limit = int(params[1]) if len(params) >= 2 else default_limit
            return page, limit
        except ValueError:
            print("Неверный формат! Используются значения по умолчанию.")
            return default_page, default_limit

    @staticmethod
    def show_main_menu() -> str:
        """Отображает главное меню и возвращает выбор пользователя."""
        print(" _________________________ ")
        print("|       FILM FINDER       |")
        print("|_________________________|")
        print("|                         |")
        print("| 1. Поиск по названию    |")
        print("| 2.   Поиск по году      |")
        print("| 3. Поиск по категории   |")
        print("| 4.  Поиск по актеру     |")
        print("| 5. Показать категории   |")
        print("| 6.    Статистика        |")
        print("| 7.       Выход          |")
        print("|_________________________|")
        print()
        choice = input("--> Ваш выбор: ").strip()
        return choice

    def handle_choice(self, choice: str) -> None:
        """Обрабатывает выбор пользователя из главного меню."""
        match choice:
            case "1":
                self.search_films()
            case "2":
                self.search_by_specific_year()
            case "3":
                self.search_by_category()
            case "4":
                self.search_by_actor()
            case "5":
                self.show_categories()
            case "6":
                self.show_statistics()
            case "7":
                self.menu_exit()
            case _:
                print("Неверный выбор!")

    def search_films(self) -> None:
        """Поиск фильмов по названию и диапазону лет."""
        min_year_db, max_year_db = self.repo.years_range()
        default_values = {
            "min_year": min_year_db,
            "max_year": max_year_db,
            "page": 1,
            "limit": 10
        }

        print("\n--- Поиск фильмов по названию ---")
        print(f"Доступные годы: {min_year_db} - {max_year_db}")
        title = input("Введите название фильма (Enter для всех): ").strip()
        print("\nДополнительные параметры (формат: min_year max_year page limit)")
        print("Пример: 2000 2020 1 10")
        print("Нажмите ENTER для значений по умолчанию")
        parameters = input("--> ").strip()

        min_year, max_year, page, limit = self._parse_years_and_pagination(
            parameters,
            default_values["min_year"],
            default_values["max_year"],
            default_values["page"],
            default_values["limit"]
        )

        if min_year > max_year:
            print(f"min_year ({min_year}) > max_year ({max_year}). Приколов не будет, меняю местами.")
            min_year, max_year = max_year, min_year

        if min_year < min_year_db:
            print(f"min_year ({min_year}) вне диапазона. Используется {min_year_db}.")
            min_year = min_year_db

        if max_year > max_year_db:
            print(f"max_year ({max_year}) вне диапазона. Используется {max_year_db}.")
            max_year = max_year_db

        print(f"\nИщем: '{title or 'все фильмы'}' ({min_year}-{max_year}), страница {page}")

        search_params = (title, min_year, max_year)
        self._paginate_result(
            search_func=self.repo.get_films,
            search_params=search_params,
            current_page=page,
            limit=limit
        )

    def search_by_specific_year(self) -> None:
        """Поиск фильмов по названию и конкретному году."""
        min_year_db, max_year_db = self.repo.years_range()
        default_values = {
            "year": max_year_db,
            "page": 1,
            "limit": 10
        }

        print("\n--- Поиск фильмов по конкретному году ---")
        print(f"Доступные годы: {min_year_db} - {max_year_db}")
        year = input("\nВведите год фильма (Enter для значения по умолчанию): ").strip()
        title = input("Введите название фильма (Enter для всех): ").strip()
        print("\nДополнительные параметры (формат: page limit)")
        print("Пример: 1 10")
        print("Нажмите ENTER для значений по умолчанию")
        parameters = input("--> ").strip()

        if year:
            try:
                year = int(year)
                if not (min_year_db <= year <= max_year_db):
                    raise ValueError
            except ValueError:
                print("Неверный формат года! Используется значение по умолчанию.")
                year = default_values["year"]
        else:
            year = default_values["year"]

        page, limit = self._parse_pagination(
            parameters,
            default_values["page"],
            default_values["limit"]
        )

        print(f"\nИщем: '{title or 'все фильмы'}' ({year}), страница {page}")

        search_params = (title, year)
        self._paginate_result(
            search_func=self.repo.get_films_by_specific_year,
            search_params=search_params,
            current_page=page,
            limit=limit
        )

    def search_by_category(self) -> None:
        """Поиск фильмов по категории."""
        min_year_db, max_year_db = self.repo.years_range()
        default_values = {
            "min_year": min_year_db,
            "max_year": max_year_db,
            "page": 1,
            "limit": 10
        }

        print("\n--- Поиск фильмов по категории ---")

        categories = self.repo.get_categories()
        if not categories:
            print("Категории не найдены")
            input("\nНажмите Enter для возврата в меню")
            return

        print(f"\nВсего категорий: {len(categories)}")
        print("=" * Menu.DISPLAY_PAGE_LENGTH)
        for i, category in enumerate(categories, 1):
            print(f"{i:2}. {category['name']}")
        print("=" * Menu.DISPLAY_PAGE_LENGTH)

        category_choice = input("\nВведите номер или название категории: ").strip()

        if category_choice.isdigit():
            idx = int(category_choice) - 1
            if 0 <= idx < len(categories):
                category = categories[idx]['name']
            else:
                print("Неверный номер категории!")
                input("\nНажмите Enter для возврата в меню")
                return
        else:
            category = category_choice

        print(f"Доступные годы: {min_year_db} - {max_year_db}")
        title = input("Введите название фильма (Enter для всех): ").strip()
        print("\nДополнительные параметры (формат: min_year max_year page limit)")
        print("Пример: 2000 2020 1 10")
        print("Нажмите ENTER для значений по умолчанию")
        parameters = input("--> ").strip()

        min_year, max_year, page, limit = self._parse_years_and_pagination(
            parameters,
            default_values["min_year"],
            default_values["max_year"],
            default_values["page"],
            default_values["limit"]
        )

        if min_year > max_year:
            print(f"min_year ({min_year}) > max_year ({max_year}). Приколов не будет, меняю местами.")
            min_year, max_year = max_year, min_year

        if min_year < min_year_db:
            print(f"min_year ({min_year}) вне диапазона. Используется {min_year_db}.")
            min_year = min_year_db

        if max_year > max_year_db:
            print(f"max_year ({max_year}) вне диапазона. Используется {max_year_db}.")
            max_year = max_year_db

        print(f"\nИщем: '{title or 'все фильмы'}' категории '{category}' ({min_year}-{max_year}), страница {page}")

        search_params = (title, min_year, max_year, category)
        self._paginate_result(
            search_func=self.repo.get_films_by_category,
            search_params=search_params,
            current_page=page,
            limit=limit
        )

    def search_by_actor(self) -> None:
        """Поиск фильмов по актёру (в разработке)."""
        pass

    def show_categories(self) -> None:
        """Отображает список всех доступных категорий."""
        print("\n--- Доступные категории ---")
        categories = self.repo.get_categories()

        if not categories:
            print("Категории не найдены")
            return

        print(f"\nВсего категорий: {len(categories)}")
        print("=" * Menu.DISPLAY_PAGE_LENGTH)

        for i, category in enumerate(categories, 1):
            print(f"{i:2}. {category['name']}")

        print("=" * Menu.DISPLAY_PAGE_LENGTH)
        input("\nНажмите Enter для возврата в меню")

    def show_statistics(self) -> None:
        """Отображает статистику запросов из MongoDB."""
        print("\n--- Статистика поисковых запросов ---")

        stats = self.repo.get_statistics()

        if not stats:
            print("Статистика недоступна (MongoDB отключен или нет данных)")
            input("\nНажмите Enter для возврата в меню")
            return

        print(f"\nВсего запросов: {stats['total']}")
        print("=" * Menu.DISPLAY_PAGE_LENGTH)

        if stats['by_type']:
            print("\nЗапросы по типам:")
            for item in stats['by_type']:
                query_type = item['_id'] or "неизвестно"
                print(f"  {query_type}: {item['count']}")

        if stats['top_titles']:
            print("\nТоп-10 поисковых запросов:")
            for i, item in enumerate(stats['top_titles'], 1):
                print(f"  {i:2}. '{item['_id']}' — {item['count']} раз(а)")

        print("=" * Menu.DISPLAY_PAGE_LENGTH)
        input("\nНажмите Enter для возврата в меню")

    @staticmethod
    def display_films(films: List[Dict[str, Any]], page: int = 1, limit: int = 10) -> None:
        """Отображает список фильмов."""
        if not films:
            print("Фильмы не найдены(")
            return

        start = (page - 1) * limit + 1
        end = start + len(films) - 1
        print(f"\nПоказаны фильмы {start}-{end} (на странице: {len(films)})")
        print("=" * Menu.DISPLAY_PAGE_LENGTH)

        for i, film in enumerate(films, 1):
            print(f"\n{i}. {film['title']}")
            print(f"   Год выпуска: {film['release_year']}")
            print(f"   Рейтинг: {film['rating']}")
            print(f"   Категории: {film['categories']}")
            if len(film['description']) > Menu.DESCRIPTION_MAX_LENGTH:
                triple_dot = "..."
                print(f"   Описание: {film['description'][:Menu.DESCRIPTION_MAX_LENGTH - 3] + triple_dot}")
            else:
                print(f"   Описание: {film['description']}")
            print("-" * Menu.DISPLAY_PAGE_LENGTH)

    def menu_exit(self) -> None:
        """Выход из приложения."""
        print("\nПока!")
        self.running = False

    def run(self) -> None:
        """Запускает главный цикл меню."""
        while self.running:
            choice = self.show_main_menu()
            self.handle_choice(choice)


from repositories.movie_repository import MovieRepository


class Menu:
    def __init__(self, repo: MovieRepository):
        self.repo = repo
        self.running = True


    @staticmethod
    def show_main_menu():
        print(" _________________________ ")
        print("|       FILM FINDER       |")
        print("|_________________________|")
        print("|                         |")
        print("| 1. Поиск по названию    |")
        print("| 2.   Поиск по году      |")
        print("| 3. Поиск по категории   |")
        print("| 4.  Поиск по актеру     |")
        print("| 5. Показать категории   |")
        print("| 6.       Выход          |")
        print("|_________________________|")
        print()
        choice = input("➤ Ваш выбор: ").strip()
        return choice


    def handle_choice(self, choice):
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
                self.menu_exit()
            case _:
                print("Неверный выбор!")

    def search_films(self):
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
        parameters = input("➤ ").strip()

        try:
            parameters = parameters.split()
            min_year = int(parameters[0]) if len(parameters) >= 1 else default_values["min_year"]
            max_year = int(parameters[1]) if len(parameters) >= 2 else default_values["max_year"]
            page = int(parameters[2]) if len(parameters) >= 3 else default_values["page"]
            limit = int(parameters[3]) if len(parameters) >= 4 else default_values["limit"]
        except ValueError:
            print("Неверный формат! Используются значения по умолчанию.")
            min_year = default_values["min_year"]
            max_year = default_values["max_year"]
            page = default_values["page"]
            limit = default_values["limit"]

        if min_year > max_year:
            print(f"min_year ({min_year}) > max_year ({max_year}). Приколов не будет, меняю местами.")
            min_year, max_year = max_year, min_year

        if min_year < min_year_db:
            print(f"min_year ({min_year}) вне диапазона. Используется {min_year_db}.")
            min_year = min_year_db

        if max_year > max_year_db:
            print(f"max_year ({max_year}) вне диапазона. Используется {max_year_db}.")
            max_year = max_year_db

        films = self.repo.get_films(title, min_year, max_year, limit, page)
        print(f"\nИщем: '{title or 'все фильмы'}' ({min_year}-{max_year}), страница {page}")
        self.display_films(films)

    def search_by_specific_year(self):
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
        parameters = input("➤ ").strip()

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

        try:
            parameters = parameters.split()
            page = int(parameters[0]) if len(parameters) >= 1 else default_values["page"]
            limit = int(parameters[1]) if len(parameters) >= 2 else default_values["limit"]
        except ValueError:
            print("Неверный формат! Используются значения по умолчанию.")
            page = default_values["page"]
            limit = default_values["limit"]

        films = self.repo.get_films_by_specific_year(title, year, limit, page)
        print(f"\nИщем: '{title or 'все фильмы'}' ({year}), страница {page}")
        self.display_films(films)


    def search_by_category(self):
        pass


    def search_by_actor(self):
        pass


    def show_categories(self):
        print("\n--- Доступные категории ---")
        categories = self.repo.get_categories()

        if not categories:
            print("Категории не найдены")
            return

        print(f"\nВсего категорий: {len(categories)}")
        print("=" * 40)

        for i, category in enumerate(categories, 1):
            print(f"{i:2}. {category['name']}")

        print("=" * 40)
        input("\nНажмите Enter для возврата в меню")


    @staticmethod
    def display_films(films):
        if not films:
            print("Фильмы не найдены(")
            return

        print(f"\nНайдено фильмов: {len(films)}")
        print("=" * 80)

        for i, film in enumerate(films, 1):
            description = (f"{film['description'][:50]}..."
                    if len(film['description']) > 50
                    else film['description'])

            print(f"{i:2}. {film['title']:30} | {film['release_year']} | {film['rating']:5} | {film['categories']}")
            print(f"    {description}")
            print("-" * 70)


    def menu_exit(self):
        print("\nПока!")
        self.running = False


    def run(self):
        while self.running:
            choice = self.show_main_menu()
            self.handle_choice(choice)

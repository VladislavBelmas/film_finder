CATEGORIES = """SELECT name FROM category ORDER BY name"""

MIN_FILM_YEAR = """SELECT MIN(release_year) AS min_year FROM film"""

MAX_FILM_YEAR = """SELECT MAX(release_year) AS max_year FROM film"""

FILMS = """
        SELECT f.film_id, f.title, f.description, f.release_year, GROUP_CONCAT(c.name SEPARATOR ', ') as categories, 
               f.rating
        FROM film f
        JOIN film_category fc
        ON f.film_id = fc.film_id
        JOIN category c 
        ON fc.category_id = c.category_id
        WHERE f.title LIKE %s AND f.release_year BETWEEN %s AND %s 
        GROUP BY f.film_id
        ORDER BY f.title
        LIMIT %s OFFSET %s
        """

FILMS_SPECIFIC_YEAR  = """
                       SELECT f.film_id, f.title, f.description, f.release_year, 
                              GROUP_CONCAT(c.name SEPARATOR ', ') as categories, f.rating
                       FROM film f
                       JOIN film_category fc
                       ON f.film_id = fc.film_id
                       JOIN category c 
                       ON fc.category_id = c.category_id
                       WHERE f.title LIKE %s AND f.release_year = %s 
                       GROUP BY f.film_id 
                       ORDER BY f.title
                       LIMIT %s OFFSET %s
                       """

FILMS_BY_CATEGORY = """
                    SELECT f.film_id, f.title, f.description, f.release_year, 
                           GROUP_CONCAT(c.name SEPARATOR ', ') as categories, f.rating
                    FROM film f
                    JOIN film_category fc
                    ON f.film_id = fc.film_id
                    JOIN category c 
                    ON fc.category_id = c.category_id
                    WHERE f.title LIKE %s AND f.release_year BETWEEN %s AND %s
                    GROUP BY f.film_id
                    HAVING FIND_IN_SET(%s, categories) > 0
                    ORDER BY f.title
                    LIMIT %s OFFSET %s     
                    """

FILMS_BY_ACTOR = """

                 """
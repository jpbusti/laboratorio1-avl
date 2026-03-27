class Node:
    def __init__(
        self,
        course_id,
        title,
        url,
        rating,
        num_reviews,
        num_published_lectures,
        created,
        last_update_date,
        duration,
        instructors_id,
        image,
        positive_reviews,
        negative_reviews,
        neutral_reviews,
    ):
        """
        Inicializa un nuevo nodo con los datos del dataset y calcula
        automáticamente su nivel de satisfacción.
        """
        # Atributos de identificación y metadatos
        self.course_id              = course_id
        self.title                  = title
        self.url                    = url
        self.rating                 = float(rating)
        self.num_reviews            = int(num_reviews)
        self.num_published_lectures = int(num_published_lectures)
        self.created                = created
        self.last_update_date       = last_update_date
        
        # Procesamiento de la duración: extrae el número del string (ej: '3.5 hours')
        try:
            self.duration = float(str(duration).split()[0])
        except (ValueError, IndexError):
            self.duration = 0.0
            
        self.instructors_id         = instructors_id
        self.image                  = image
        self.positive_reviews       = int(positive_reviews)
        self.negative_reviews       = int(negative_reviews)
        self.neutral_reviews        = int(neutral_reviews)
 
        # Cálculo de la métrica principal para el ordenamiento del árbol
        self.satisfaction = self._calculate_satisfaction()
 
        # Referencias de la estructura de datos
        self.left   = None   # Puntero al hijo izquierdo
        self.right  = None   # Puntero al hijo derecho
        self.height = 1      # Altura del nodo (inicializada en 1 por ser una hoja)
 
    def _calculate_satisfaction(self):
        """
        Calcula el nivel de satisfacción del curso basándose en una ponderación:
        """
        if self.num_reviews == 0:
            review_score = 0.0
        else:
            # Fórmula de puntaje ponderado de reseñas:
            # (5 * positivas + 3 * neutrales + 1 * negativas) / total_reseñas
            review_score = (
                (5 * self.positive_reviews
                 + 3 * self.neutral_reviews
                 + self.negative_reviews)
                / self.num_reviews
            )
 
        # Cálculo final combinando el rating y el puntaje de reseñas
        satisfaction = self.rating * 0.7 + review_score * 0.3
        return round(satisfaction, 5)
    
    def __str__(self):
        """Retorna una representación legible del nodo para depuración."""
        return (
            f"ID: {self.course_id} | "
            f"Título: {self.title} | "
            f"Satisfacción: {self.satisfaction} | "
            f"Altura: {self.height}"
        )
 
    def get_info(self):
        """
        Retorna un diccionario con toda la información del curso.
        Útil para mostrar los detalles en la interfaz gráfica.
        """
        return {
            "course_id"             : self.course_id,
            "title"                 : self.title,
            "url"                   : self.url,
            "rating"                : self.rating,
            "num_reviews"           : self.num_reviews,
            "num_published_lectures": self.num_published_lectures,
            "created"               : self.created,
            "last_update_date"      : self.last_update_date,
            "duration"              : self.duration,
            "instructors_id"        : self.instructors_id,
            "image"                 : self.image,
            "positive_reviews"      : self.positive_reviews,
            "negative_reviews"      : self.negative_reviews,
            "neutral_reviews"       : self.neutral_reviews,
            "satisfaction"          : self.satisfaction,
            "height"                : self.height,
        }
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
        self.course_id              = course_id
        self.title                  = title
        self.url                    = url
        self.rating                 = float(rating)
        self.num_reviews            = int(num_reviews)
        self.num_published_lectures = int(num_published_lectures)
        self.created                = created
        self.last_update_date       = last_update_date
        self.duration               = float(duration) if duration else 0.0
        self.instructors_id         = instructors_id
        self.image                  = image
        self.positive_reviews       = int(positive_reviews)
        self.negative_reviews       = int(negative_reviews)
        self.neutral_reviews        = int(neutral_reviews)
 
        self.satisfaction = self._calculate_satisfaction()
 
        self.left   = None   
        self.right  = None   
        self.height = 1      
 
 
    def _calculate_satisfaction(self):
        if self.num_reviews == 0:
            review_score = 0.0
        else:
            review_score = (
                (5 * self.positive_reviews
                 + 3 * self.neutral_reviews
                 + self.negative_reviews)
                / self.num_reviews
            )
 
        satisfaction = self.rating * 0.7 + review_score * 0.3
        return round(satisfaction, 5)
    
    def __str__(self):

        return (
            f"ID: {self.course_id} | "
            f"Título: {self.title} | "
            f"Satisfacción: {self.satisfaction} | "
            f"Altura: {self.height}"
        )
 
    def get_info(self):

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
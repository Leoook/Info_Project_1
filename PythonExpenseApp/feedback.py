class Feedback:
    _id_counter = 1

    def __init__(self, student, activity, rating, comment):
        self.id = Feedback._id_counter
        Feedback._id_counter += 1
        self.student = student
        self.activity = activity
        self.rating = rating
        self.comment = comment

    def get_id(self):
        return self.id

    def get_student(self):
        return self.student

    def get_activity(self):
        return self.activity

    def get_rating(self):
        return self.rating

    def get_comment(self):
        return self.comment

    def __str__(self):
        return f"Feedback(id={self.id}, rating={self.rating}, comment='{self.comment}')"
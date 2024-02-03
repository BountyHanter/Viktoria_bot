class Info:
    def __init__(self):
        self.name = None
        self.second_name = None
        self.city = None
        self.job_title = None
        self.tenchat_link = None
        self.comment = None
        self.comment_to_discus = None
        self.deal_id = None
        self.company_name = None
        self.id_number = None

    def to_dict(self):
        return {
            'name': self.name,
            'second_name': self.second_name,
            'city': self.city,
            'job_title': self.job_title,
            'tenchat_link': self.tenchat_link,
            'comment': self.comment,
            'comment_to_discus': self.comment_to_discus,
            'deal_id': self.deal_id,
            'company_name': self.company_name,
            'id_number': self.id_number
        }
class infoTemplateMapping:
    id = int
    mapping = str
    template_id = int

    def __init__(self, id, template_id, mapping):
        self.id = id
        self.template_id = template_id
        self.mapping = mapping

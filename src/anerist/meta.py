
class validator():
    def validate(self, data=None):
        if not data:
            print("no metadata available, validation failed.")
            sys.exit(1)
        essential_attributes = [
                'title',
                'slug',
                'lang',
                ]
        if all(attribute in data for attribute in essential_attributes):
            return True

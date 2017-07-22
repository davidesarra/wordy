class Interface(object):
    @staticmethod
    def _get_non_empty_input(message):
        while True:
            value = input(message)
            if not value:
                continue
            return value

    def get_input(self, message, mandatory):
        if mandatory:
            return self._get_non_empty_input(message=message)
        return input(message)

    def get_string(self, message, mandatory):
        return self.get_input(message=message, mandatory=mandatory)

    def get_integer(self, message, mandatory):
        while True:
            try:
                raw_value = self.get_input(message=message, mandatory=mandatory)
                if raw_value == "":
                    return None
                return int(raw_value)
            except ValueError:
                continue

    def get_boolean(self, message, true_values, false_values):
        while True:
            value = self.get_input(message=message, mandatory=True)
            if value in true_values:
                return True
            elif value in false_values:
                return False
            print(
                f"Allowed true values: {true_values}, " f"false values {false_values}"
            )

    def get_list_of_strings(self, message, separator, strip_whitespace, mandatory):
        raw_value = self.get_input(message=message, mandatory=mandatory)
        if raw_value:
            return [
                entry if not strip_whitespace else entry.strip()
                for entry in raw_value.split(sep=separator, maxsplit=-1)
            ]
        return []

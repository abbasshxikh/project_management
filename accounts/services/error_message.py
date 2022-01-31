class ErrorMessage:
    @classmethod
    def get_error_message_list(cls, message):
        """extend message objects all errors in list"""
        error_list = []
        for key, value in message.items():
            if isinstance(value, list):
                if "[" and "]" in value[0]:
                    replace_value = value[0]
                    replace_value = (
                        replace_value.replace("[", "").replace("]", "").replace("'", "")
                    )
                    error_list.append(replace_value)
                else:
                    error_list.extend(value)
            else:
                error_list.append(value)
        return error_list


class AT:

    async def send_message(self, message: str, number: str, publish, transport, wait_for_reply):
        # Change the Mode to Text Mode
        end_of_sms = 'EOSS'
        topic = 'input'
        m = 'AT+CMGF=1'
        publish(topic, m, transport)
        # Set the GSM Module in Text Mode
        m = 'AT+CMGS="' + number + '"'
        publish(topic, m, transport)
        # Wait for the '>' character
        await wait_for_reply

        # Send a message to a particular Number
        publish(topic, message, transport)
        publish(topic, end_of_sms, transport)

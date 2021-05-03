import requests as req


async def add_prediction_feedback(payload, message):

    if payload.emoji.name == '✔️':
        vote = 1
    elif payload.emoji.name == '❌':
        vote = -1
    else:
        #Thanks for the enthusiasm, but not what we're looking for.
        return

    prediction_data = extract_prediction(message)

    prediction = {
        "discord_id":   payload.user_id,
        "name":         prediction_data[0],
        "prediction":   prediction_data[1],
        "confidence":   prediction_data[2],
        "vote":         vote
    }

    endpoint = "https://www.osrsbotdetector.com/api/discord/predictionfeedback/"

    request = req.post(endpoint, json=prediction)

    return


def extract_prediction(message):
    name_substring = "+ Name: "
    prediction_substring = "Prediction: "
    confidence_substring = "Confidence: "

    message_lines = message.content.splitlines()

    name_line = [i for i in message_lines if name_substring in i]
    prediction_line = [i for i in message_lines if prediction_substring in i]
    confidence_line = [i for i in message_lines if confidence_substring in i]

    name = name_line[0].split(name_substring)[1]
    prediction = prediction_line[0].split(prediction_substring)[1]
    confidence = confidence_line[0].split(confidence_substring)[1]

    return name, prediction, float(confidence)
from transformers import BertTokenizer, BertForSequenceClassification
import torch


model_path = "bert_emotion_model"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def predici_emozione(testo):
    inputs = tokenizer(testo, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    emotion_dict = {
        0: 'ammirazione',
        2: 'rabbia',
        6: 'confusione',
        10: 'disapprovazione',
        11: 'disgusto',
        14: 'paura',
        17: 'gioia',
        25: 'tristezza',
        27: 'neutra'
    }
    return emotion_dict[prediction]

#example string
messaggio_test = ""
print("Emozione rilevata:", predici_emozione(messaggio_test))
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import AdamW, get_scheduler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tqdm import tqdm

# Caricamento del dataset con intestazioni numeriche
df = pd.read_csv('../dataset_finale_bilanciato.csv', header=None)

# Rinomina le colonne per chiarezza
df.columns = ['messaggio', 'emozione']

# Mappatura delle emozioni in numeri (aggiornato in base alla colonna corretta)
emotions_mapping = {
    0: 'ammirazione', 1: 'divertimento', 2: 'rabbia', 3: 'fastidio', 4: 'approvazione',
    5: 'premura', 6: 'confusione', 7: 'curiosità', 8: 'desiderio', 9: 'delusione',
    10: 'disapprovazione', 11: 'disgusto', 12: 'imbarazzo', 13: 'entusiasmo', 14: 'paura',
    15: 'gratitudine', 16: 'dolore', 17: 'gioia', 18: 'amore', 19: 'nervosismo',
    20: 'ottimismo', 21: 'orgoglio', 22: 'consapevolezza', 23: 'sollievo', 24: 'rimorso',
    25: 'tristezza', 26: 'sorpresa', 27: 'neutra'
}

# Mappatura corretta nel dataframe
df['emozione'] = df['emozione'].astype(int)  # Assicuriamoci che sia un valore numerico

# Pulizia e tokenizzazione del testo
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


class EmotionDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = tokenizer(
            self.texts[idx],
            padding='max_length',
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }


# Divisione train-test
X_train, X_test, y_train, y_test = train_test_split(df['messaggio'].tolist(), df['emozione'].tolist(), test_size=0.2,
                                                    random_state=42)

train_dataset = EmotionDataset(X_train, y_train)
test_dataset = EmotionDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

# Caricamento del modello pre-addestrato BERT
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(emotions_mapping))

# Configurazione del dispositivo (GPU se disponibile)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Definizione della funzione di perdita e dell'ottimizzatore
optimizer = AdamW(model.parameters(), lr=2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

# Scheduler per il controllo del learning rate
num_training_steps = len(train_loader) * 3
lr_scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)

# Addestramento del modello
epochs = 3
for epoch in range(epochs):
    model.train()
    total_loss = 0

    for batch in tqdm(train_loader):
        input_ids, attention_mask, labels = batch['input_ids'].to(device), batch['attention_mask'].to(device), batch[
            'labels'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask)
        loss = loss_fn(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_loader):.4f}")

# Valutazione del modello
model.eval()
predictions, true_labels = [], []

with torch.no_grad():
    for batch in test_loader:
        input_ids, attention_mask, labels = batch['input_ids'].to(device), batch['attention_mask'].to(device), batch[
            'labels'].to(device)

        outputs = model(input_ids, attention_mask=attention_mask)
        preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
        predictions.extend(preds)
        true_labels.extend(labels.cpu().numpy())

# Calcolo dell'accuratezza
accuracy = accuracy_score(true_labels, predictions)
print(f'Accuratezza del modello: {accuracy:.2f}')

# Salvataggio del modello addestrato
model.save_pretrained("bert_emotion_model")
tokenizer.save_pretrained("bert_emotion_model")
print("Modello addestrato e salvato con successo!")

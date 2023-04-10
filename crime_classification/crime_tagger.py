
    
import numpy as np
import torch 
from transformers import XLMRobertaTokenizer
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch.nn.functional as F
from transformers import XLMRobertaForSequenceClassification
import torch.nn as nn
import torch

class XLMRClassifier:
    def __init__(self, model_path, premodel='xlm-roberta-large', max_len=500, batch_size=32):
        self.model_path = model_path
        self.premodel = premodel
        self.max_len = max_len
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(self.premodel)
        self.model = self._load_model()
    
    def _load_model(self):
        model = XLMRobertaForSequenceClassification.from_pretrained(self.premodel,num_labels=8,output_attentions=False,output_hidden_states=False)
        model = nn.DataParallel(model)
        model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
        model.to(self.device)
        model.eval()
        return model
    
    def preprocess(self, data):
        input_ids = []
        attention_masks = []

        for sent in data:
            encoded_sent = self.tokenizer.encode_plus(
                text=sent,
                add_special_tokens=True,        
                max_length=self.max_len,
                truncation=True,             
                padding='max_length',         
                return_attention_mask=True      
            )

            input_ids.append(encoded_sent.get('input_ids'))
            attention_masks.append(encoded_sent.get('attention_mask'))

        input_ids = torch.tensor(input_ids)
        attention_masks = torch.tensor(attention_masks)

        return input_ids, attention_masks
    
    def predict(self, data):
        inputs, masks = self.preprocess(data)
        dataset = TensorDataset(inputs, masks)
        sampler = SequentialSampler(dataset)
        dataloader = DataLoader(dataset, sampler=sampler, batch_size=self.batch_size)
        probs = self._predict(self.model, dataloader)
        return probs
    
    def _predict(self, model, dataloader):
        model.eval()

        all_logits = []

        for batch in dataloader:
            b_input_ids, b_attn_mask = tuple(t.to(self.device) for t in batch)[:2]

            with torch.no_grad():
                outputs = model(b_input_ids, b_attn_mask)
                logits = outputs.logits
            all_logits.append(logits)

        all_logits = torch.cat(all_logits, dim=0)
        probs = all_logits.sigmoid().cpu().numpy()

        threshold_set = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.1]
        probs[...,0] = np.where(probs[...,0] > threshold_set[1],1,0)
        probs[...,1] = np.where(probs[...,1] > threshold_set[1],1,0)
        probs[...,2] = np.where(probs[...,2] > threshold_set[2],1,0)
        probs[...,3] = np.where(probs[...,3] > threshold_set[3],1,0)
        probs[...,4] = np.where(probs[...,4] > threshold_set[4],1,0)
        probs[...,5] = np.where(probs[...,5] > threshold_set[5],1,0)
        probs[...,6] = np.where(probs[...,6] > threshold_set[6],1,0)
        probs[...,7] = np.where(probs[...,7] > threshold_set[7],1,0)

        return probs


# def main():
#     XLMR_path = "./XLMR_Model.h5"
#     XLMR_chosen_premodel = 'xlm-roberta-large'
#     classifier = XLMRClassifier(XLMR_path, XLMR_chosen_premodel)

#     # example usage
#     merge_all_news = [("title 1", "description 1", "text 1"), ("title 2", "description 2", "text 2")]
#     probs = classifier.predict([news[2] for news in merge_all_news])
#     print(probs)
    
# if __name__ == "__main__":
#     main()

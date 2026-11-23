"""Small, reproducible educational experiment. See README for limitations."""
import json
from pathlib import Path
import numpy as np

def save(result, output):
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

def run(output="results.json"):
    X,y=load_digits(return_X_y=True)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,random_state=42))
    pred=m.fit(Xtr,ytr).predict(Xte)
    cm=confusion_matrix(yte,pred)
    pairs=sorted([(int(cm[a,b]),a,b) for a in range(10) for b in range(10) if a!=b],reverse=True)[:5]
    base=DummyClassifier(strategy="most_frequent").fit(Xtr,ytr).predict(Xte)
    return save({"seed":42,"train_rows":len(ytr),"test_rows":len(yte),"accuracy":float(accuracy_score(yte,pred)),"macro_f1":float(f1_score(yte,pred,average="macro")),"majority_accuracy":float(accuracy_score(yte,base)),"confusion_matrix":cm.tolist(),"top_confusions":[{"count":n,"actual":a,"predicted":b} for n,a,b in pairs]},output)

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

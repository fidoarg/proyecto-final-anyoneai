import pandas as pd
import matplotlib.pyplot as plt

from sklearn import metrics


def get_performance(predictions, y_test, labels=[1, 0]):
    # Put your code
    accuracy = metrics.accuracy_score(
            y_pred=predictions, y_true=y_test
    )
    precision = metrics.precision_score(
            y_pred=predictions, y_true=y_test
    )
    recall = metrics.recall_score(
            y_pred=predictions, y_true=y_test
    )
    f1_score = metrics.f1_score(
            y_pred=predictions, y_true=y_test
    )
    
    report = metrics.classification_report(
            y_true=y_test, y_pred=predictions
    )

    # Confusion matrix
    cm = metrics.confusion_matrix(
            y_true=y_test, y_pred=predictions
    )
    cm_as_dataframe = pd.DataFrame(data=cm)
    
    print('Model Performance metrics:')
    print('-'*30)
    print('Accuracy:', round(accuracy, 4))
    print('Precision:', round(precision, 4))
    print('Recall:', round(recall, 4))
    print('F1 Score:', round(f1_score, 4))
    print('\nModel Classification report:')
    print('-'*30)
    print(report)
    print('\nPrediction Confusion Matrix:')
    print('-'*30)
    print(cm_as_dataframe)
    
    return accuracy, precision, recall, f1_score


def plot_roc(model, y_test, features):
    # Put your code
    fpr = metrics.roc_curve(
            y_true=y_test,
            y_score=model.predict_proba(features)[:, 1],
    )[0]
    tpr = metrics.roc_curve(
            y_true=y_test,
            y_score=model.predict_proba(features)[:, 1],
            pos_label=1
    )[1]
    roc_auc = metrics.roc_auc_score(
            y_true=y_test, y_score=model.predict_proba(features)[:, 1]
    )

    plt.figure(figsize=(10, 5))
    plt.plot(fpr, tpr, label=f'ROC curve (area = {roc_auc})', linewidth=2.5)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

    return roc_auc
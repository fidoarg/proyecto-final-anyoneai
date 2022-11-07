import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from sklearn.metrics import (accuracy_score,
                             classification_report,
                             confusion_matrix,
                             f1_score,
                             precision_score,
                             recall_score,
                             roc_auc_score,
                             roc_curve
                             )
from sklearn.utils.validation import check_is_fitted
from time import time

def get_performance(predictions, y_true, predictions_probas, labels=[1, 0]):
    """

    :param predictions:
    :param y_true:
    :param labels:
    :return:
    """


    accuracy  = round(accuracy_score(y_pred=predictions, y_true=y_true), 4)
    precision = round(precision_score(y_pred=predictions, y_true=y_true), 4)
    recall    = round(recall_score(y_pred=predictions, y_true=y_true), 4)
    f1        = round(f1_score(y_pred=predictions, y_true=y_true), 4)
    roc_auc   = round(
                      roc_auc_score(y_true=y_true,
                                    y_score=predictions_probas[:, 1]), 4)
    report = classification_report(y_true=y_true, y_pred=predictions)

    # Confusion matrix
    cm = confusion_matrix(y_true=y_true, y_pred=predictions)
    cm_as_dataframe = pd.DataFrame(data=cm)

    # Displaying information when function called
    print('Model Performance metrics:')
    print('-'*30)
    print('Accuracy:', accuracy)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1 Score:', f1)
    print('Roc-Auc Score:', roc_auc)
    print('\nModel Classification report:')
    print('-'*30)
    print(report)
    print('\nPrediction Confusion Matrix:')
    print('-'*30)
    print(cm_as_dataframe)
    
    # ROC-AUC Curve
    fpr = roc_curve(
            y_true=y_true,
            y_score=predictions_probas[:, 1],
    )[0]
    tpr = roc_curve(
            y_true=y_true,
            y_score=predictions_probas[:, 1],
            pos_label=1
    )[1]


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

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall' : recall,
        'f1': f1,
        'roc_auc': roc_auc
    }

def make_experiment(model,
                    alg_name,
                    data_dir,
                    X_train,
                    y_train,
                    X_val,
                    y_val,
                    X_test=None,
                    y_test=None,
                    CV_search=False):
    """

    :param model:
    :param alg_name:
    :param X_train:
    :param y_train:
    :param X_val:
    :param y_val:
    :param X_test:
    :param y_test:
    :param CV_search:
    :return:
    """

    # Train the model
    ini_time = time()
    model.fit(X=X_train, y=y_train)
    train_time = round(time() - ini_time, 4)

    # Make prediction over validation set
    ini_time = time()
    preds = model.predict(X=X_val)
    preds_probas = model.predict_proba(X=X_val)
    val_pred_time = round(time() - ini_time, 4)

    # Get model performance metrics over validation set
    val_metrics = get_performance(predictions=preds,
                                  y_true=y_val,
                                  predictions_probas=preds_probas)

    # Define experiment number
    exp_num = 0
    # Define model name and parameters depending on CV_search parameter
    if CV_search:
        # Set model name
        model_name = alg_name + '_hpo'
        # Get model parameters that gave the best result on search
        model_parameters = model.best_estimator_.get_params()
        # Make prediction over test set
        ini_time = time()
        preds = model.predict(X=X_test)
        preds_probas = model.predict_proba(X=X_test)
        test_pred_time = round(time() - ini_time, 4)

        # Get model performance metrics over validation set
        test_metrics = get_performance(predictions=preds,
                                      y_true=y_test,
                                      predictions_probas=preds_probas)

    else:
        model_name = alg_name
        model_parameters = model.get_params()
        test_pred_time = '-'
        test_metrics = {
            'accuracy': '-',
            'precision': '-',
            'recall' : '-',
            'f1': '-',
            'roc_auc': '-'
        }
    # Store results as dictionaries and save them to a json file
    results = {
        'model_name': model_name,
        'model_params': model_parameters,
        'data_dir': data_dir.split('/')[-1],
        'val_accuracy': val_metrics['accuracy'],
        'val_precision': val_metrics['precision'],
        'val_recall' : val_metrics['recall'],
        'val_f1': val_metrics['f1'],
        'val_roc_auc': val_metrics['roc_auc'],
        'test_accuracy': test_metrics['accuracy'],
        'test_precision': test_metrics['precision'],
        'test_recall' : test_metrics['recall'],
        'test_f1': test_metrics['f1'],
        'test_roc_auc': test_metrics['roc_auc'],
        'training_time': train_time,
        'val_pred_time': val_pred_time,
        'test_pred_time': test_pred_time
    }
    #%% Save results
    # Make experiments directory if it doesn't exist
    os.makedirs("../experiments", exist_ok=True)
    # Set experiment path
    if len(os.listdir('../experiments')) < 10:
        exp_path = 'exp_' + '00' + str(int(len(os.listdir('../experiments'))))
    elif len(os.listdir('../experiments')) < 100:
        exp_path = 'exp_' + '0' + str(int(len(os.listdir('../experiments'))))
    else:
        exp_path = 'exp_' + str(int(len(os.listdir('../experiments'))))

    # Create experiment directory
    os.makedirs(os.path.join('../experiments', exp_path), exist_ok=True)
    # Store in JSON format
    with open(os.path.join('../experiments', exp_path,'results.json'),'w') as f:
        json.dump(results, f, indent=4)

    # Print results
    print('The times of this experiment are:')
    print('\nTIMES\n')
    print(f'Training took: {results["training_time"]}')
    print(f'Prediction on Validation set took: {results["val_pred_time"]}')
    print(f'Prediction on Test set took: {results["test_pred_time"]}')

    # Return fitted model for future uses
    return model
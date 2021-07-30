import json
from pytablewriter import MarkdownTableWriter


def publish_report(report,gral_values=[], value_name= ""):
    keys = list(report)
    keys = [key for key in report if key not in gral_values]
    metric = [report[key] for key in keys]
    metric_keys = list(metric[0].keys())

    writer = MarkdownTableWriter()
    writer.table_name = "{} Performance Report".format(value_name)
    writer.headers = [value_name]+metric_keys
    writer.value_matrix = [[keys[index]]+[report[o_key][i_key] for i_key in metric_keys] for index, o_key in enumerate(keys,0)]
    writer.margin = 1  # add a whitespace for both sides of each cell
    writer.dump('{}_report.md'.format(value_name))
    print("script executed {} table created".format(value_name))

def main():
    with open('intent_report.json', 'r') as file:
        report = json.load(file)
        gral_values = ['accuracy', 'macro avg', 'weighted avg']
        publish_report(report, gral_values, "intent")

    with open('story_report.json', 'r') as file:
        report = json.load(file)
        gral_values = ['accuracy','macro avg', 'weighted avg', 'conversation_accuracy']
        publish_report(report, gral_values, "story")

    with open('DIETClassifier_report.json', 'r') as file:
        report = json.load(file)
        gral_values = ['micro avg','macro avg', 'weighted avg']
        publish_report(report, gral_values, "DIETClassifier")

    with open('TEDPolicy_report.json', 'r') as file:
        report = json.load(file)
        gral_values = ['micro avg','macro avg', 'weighted avg']
        publish_report(report, gral_values, "TEDPolicy")
    

if __name__ == "__main__":
    main()
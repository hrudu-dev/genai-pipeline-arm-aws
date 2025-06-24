from data_processing import preprocess_data
from inference import run_inference

def main():
    data = preprocess_data("data/input.csv")
    results = run_inference(data)
    print(results)

if __name__ == "__main__":
    main()
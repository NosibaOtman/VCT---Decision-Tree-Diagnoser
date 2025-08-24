# Decision Tree Diagnoser

This repository contains a Python implementation of a **Decision Tree Diagnoser** for illnesses based on symptoms. It allows creating, traversing, and optimizing decision trees to determine diseases given a set of symptoms.

## Features

- **Decision Tree Structure:** Implemented using a `Node` class, where each node represents a question (symptom) or a leaf (diagnosis).  
- **Records Handling:** `Record` class stores illnesses and their corresponding symptoms.  
- **Diagnoser:** The `Diagnoser` class provides methods to:
  - Diagnose a patient based on symptoms (`diagnose`).  
  - Calculate the success rate of the decision tree (`calculate_success_rate`).  
  - Retrieve all illnesses stored in the tree (`all_illnesses`).  
  - Find all paths to a specific illness (`paths_to_illness`).  
  - Minimize the decision tree (`minimize`).  
- **Tree Construction:**  
  - Build a decision tree from records and a list of symptoms (`build_tree`).  
  - Find the optimal tree with a given depth for maximum success rate (`optimal_tree`).  

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone the repository:  
```bash
git clone https://github.com/your-username/vct.git

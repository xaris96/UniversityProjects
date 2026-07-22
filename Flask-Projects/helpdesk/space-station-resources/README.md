# Space Station Resources CRUD Application

This project is a Flask-based web application that manages the stock of resources for a space station. It provides a simple interface for creating, reading, updating, and deleting resource entries.

## Features

- Add new resources to the inventory
- View a list of all resources
- Edit existing resources
- Delete resources from the inventory

## Project Structure

```
space-station-resources
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── add_resource.html
│   │   └── edit_resource.html
│   └── static
│       ├── css
│       │   └── styles.css
│       └── js
│           └── scripts.js
├── migrations
├── .gitignore
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd space-station-resources
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Initialize the database locally:
   ```
   python run.py init-db
   ```

2. Run the application:
   ```
   python run.py
   ```

3. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Portfolio Cleanup
Runtime SQLite databases are not included in this portfolio copy. Recreate them locally with the initialization command above.

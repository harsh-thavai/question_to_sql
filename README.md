# Natural Language to SQL Query Generator

This project is a Streamlit-based web application that converts natural language questions into SQL queries for inventory management. It specifically interfaces with the AtliQ T-Shirts database but can be adapted for other inventory systems. The application leverages Google's Generative AI to transform user questions into SQL queries, which are then executed against the database.

![image](https://github.com/user-attachments/assets/ad1abe7d-dfc4-4ec7-9989-07dd04ed33f4)


## Features

- Natural language interface for querying inventory data
- Conversion of questions to SQL using Google's Generative AI
- Real-time database querying and result display
- Configurable database connection settings
- Specialized for the AtliQ T-Shirts inventory database

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- MySQL database (AtliQ T-Shirts inventory data)
- Google Cloud account with access to the Generative AI API

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/harsh-thavai/question_to_sql.git
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the project root:
   ```
   DB_HOST=your_database_host
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_NAME=atliq_tshirts
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).

3. Use the sidebar to input your database connection details if they're not already set in the `.env` file.

4. In the main area, enter your question about the T-shirt inventory in natural language.

5. Click "Ask the question" to generate and execute the SQL query.

6. View the generated SQL query and the query results displayed on the page.

## Example Questions

Here are some example questions you can ask:

1. "How many t-shirts do we have in total?"
2. "What is the total value of Nike t-shirts in stock?"
3. "How many white Levi's t-shirts are available in size M?"

The application will convert these questions into appropriate SQL queries for the AtliQ T-Shirts database.

## Project Structure

- `app.py`: The main Streamlit application file
- `requirements.txt`: List of Python package dependencies
- `.env`: Environment variables file (not tracked in git)

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

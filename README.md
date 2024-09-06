# Intelligent Email Summarization and Processing Tool

## Overview

This project is an advanced email processing and summarization tool designed to enhance productivity and streamline email management. The application leverages cutting-edge natural language processing (NLP) models to automatically retrieve, analyze, and summarize email content, providing users with concise and actionable insights—all while running locally to ensure data privacy and security.

## Features

- **Automated Email Retrieval**: Seamlessly connects to IMAP email servers to fetch emails in real-time.
- **Advanced Summarization**: Utilizes large language models (e.g., LLaMA) to generate concise summaries of lengthy emails.
- **Local Processing**: Runs entirely on local machines, ensuring that no email data is sent to the cloud, thereby eliminating potential data leaks.
- **Configurable Settings**: Environment variable-based configuration for flexible and secure deployment.
- **Security**: Implements efficient memory management through CPU offloading and supports SSL for secure communication.

## Technologies Used

- **Programming Languages**: Python
- **Libraries**: Hugging Face Transformers, BitsAndBytes, dotenv
- **NLP Models**: Large language models (e.g., LLaMA)
- **Deployment**: Configurable via environment variables

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/email-summarization-tool.git
    cd email-summarization-tool
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory of the project.
    - Add the following environment variables:
        ```env
        AI_MODEL=your_model_name
        EMAIL_FETCH_COMMAND=(RFC822)
        ```

## Usage

1. Run the application:
    ```sh
    python src/model_server.py
    ```

2. The application will start and connect to the specified IMAP email server to fetch and summarize emails.

## Configuration

- **AI_MODEL**: The name of the NLP model to use for summarization.
- **EMAIL_FETCH_COMMAND**: The command used to fetch emails from the IMAP server.

## Security

This tool runs entirely on local machines, ensuring that no email data is sent to the cloud, thereby eliminating potential data leaks. It also supports SSL for secure communication and implements efficient memory management through CPU offloading.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License



This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact [jtorresuci@gmail.com](mailto:jtorresuci@gmail.com).

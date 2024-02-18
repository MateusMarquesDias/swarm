pipeline {
    agent any
    
    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/seu-usuario/seu-repositorio'
            }
        }
        
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt' // Instala as dependências
            }
        }
        
        stage('Test') {
            steps {
                sh 'python -m pytest tests/test_app.py' // Executa os testes
            }
        }
    }
}

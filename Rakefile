require 'rake'

namespace :app do
  desc "Construir la imagen Docker"
  task :build do
    sh "docker-compose build"
  end

  desc "Iniciar la aplicación"
  task :start do
    sh "docker-compose up -d"
  end

  desc "Detener la aplicación"
  task :stop do
    sh "docker-compose down"
  end

  desc "Ver logs de la aplicación"
  task :logs do
    sh "docker-compose logs -f"
  end

  desc "Limpiar archivos temporales y caché"
  task :clean do
    sh "find . -type d -name '__pycache__' -exec rm -r {} +"
    sh "find . -type f -name '*.pyc' -delete"
  end

  desc "Verificar estado de la aplicación"
  task :status do
    sh "docker-compose ps"
  end

  desc "Acceder al shell del contenedor"
  task :shell do
    sh "docker-compose exec web bash"
  end
end

namespace :monitor do
  desc "Monitorear uso de CPU y memoria"
  task :resources do
    sh "docker stats"
  end

  desc "Verificar logs de errores"
  task :errors do
    sh "docker-compose logs -f | grep -i error"
  end
end
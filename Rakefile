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

  desc "Reiniciar completamente la aplicación (incluyendo volúmenes)"
  task :reset do
    sh "docker-compose down -v"
    Rake::Task["app:clean"].execute
    sh "docker-compose build --no-cache"
    sh "docker-compose up -d"
  end

  desc "Verificar y corregir permisos"
  task :fix_permissions do
    puts "Verificando permisos..."
    sh "mkdir -p config credentials"
    sh "chmod -R 777 config credentials"
    sh "touch config/verification_codes.yaml"
    sh "chmod 666 config/verification_codes.yaml"
    puts "Permisos corregidos"
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

  desc "Verificar permisos de archivos importantes"
  task :permissions do
    puts "\nPermisos de directorios:"
    sh "ls -la config credentials"
    puts "\nPermisos de archivos:"
    sh "ls -la config/verification_codes.yaml credentials/token.pickle 2>/dev/null || true"
  end
end
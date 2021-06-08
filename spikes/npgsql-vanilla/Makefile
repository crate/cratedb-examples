DOTNET_FRAMEWORK=net5.0

help:
	@echo "Please choose one of the following targets: start-cratedb, build, run"
	@exit 2
        
start-cratedb:
	docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:4.5.1

build:
	dotnet build

run:
	dotnet run --framework=${DOTNET_FRAMEWORK}

test:
	dotnet test --framework=${DOTNET_FRAMEWORK} --verbosity=minimal
	@#dotnet test --verbosity=normal

coverage:
	dotnet test --framework=${DOTNET_FRAMEWORK} --verbosity=minimal --collect:"XPlat Code Coverage"

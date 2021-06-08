help:
	@echo "Please choose one of the following targets: start-cratedb, build, run"
	@exit 2
        
start-cratedb:
	docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:4.5.1

build:
	dotnet build

run:
	dotnet run

test:
	dotnet test --verbosity=minimal
	@#dotnet test --verbosity=normal

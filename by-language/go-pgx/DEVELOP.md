# Maintenance

A few project maintenance commands.

Invoke linter.
```shell
gofmt -l -d .
```

Format code.
```shell
gofmt -w .
```

Display available minor and patch upgrades for all direct and indirect dependencies.
```shell
go list -u -m all
```

Update to the latest patch releases, including test dependencies.
```shell
go get -u=patch -t
go mod tidy
```

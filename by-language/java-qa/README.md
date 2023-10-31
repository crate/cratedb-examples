# JDBC QA tests


## About

Ported from https://github.com/crate/crate-qa/pull/278.


## Why?

- To have more integration tests, and keep them, running against CrateDB nightly.
- To constantly monitor that corresponding test cases don't break, even when
  underlying software versions change. In this case, regular updates to `pom.xml`
  will be driven by GitHub's Dependabot, and Java versions can be added as they
  become available on runners or through corresponding setup recipes.


## pom.xml

The `pom.xml` was generated with `mvn archetype:generate`.
```shell
mvn archetype:generate \
  -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false \
  -DgroupId=io.crate -DartifactId=jdbc-qa
```

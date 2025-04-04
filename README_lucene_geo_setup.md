
# README: Installing and Running lucene-geo-gazetteer with Maven

This guide documents the complete process for installing Maven and building the `lucene-geo-gazetteer` Java project, including handling common errors and launching the application.

---

## 🛠️ Environment Setup

### 1. Install Java (JDK 17)

```bash
brew install --cask temurin17
```

Or using SDKMAN:

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 17.0.9-tem
sdk use java 17.0.9-tem
```

Verify Java version:

```bash
java -version
```

Expected output:

```
java version "17.0.12" ...
```

---

### 2. Install Maven (v3.9.9 or similar)

```bash
brew install maven
```

Or manually:

- Download from https://maven.apache.org/download.cgi
- Unzip and add to your path:

```bash
export M2_HOME=~/apache-maven-3.9.9
export PATH="$M2_HOME/bin:$PATH"
```

Verify Maven version:

```bash
mvn -version
```

---

## 📦 Clone and Prepare lucene-geo-gazetteer

```bash
git clone https://github.com/chrismattmann/lucene-geo-gazetteer.git
cd lucene-geo-gazetteer
```

### Optional: Add bin to PATH

```bash
export PATH="$HOME/lucene-geo-gazetteer/src/main/bin:$PATH"
```

---

## ⚙️ Modify `pom.xml`

### 1. Use Java 11 or 17 in `maven-compiler-plugin`

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <version>3.11.0</version>
  <configuration>
    <release>11</release>
  </configuration>
</plugin>
```

### 2. Add `maven-assembly-plugin` to build a fat JAR

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-assembly-plugin</artifactId>
  <version>3.3.0</version>
  <configuration>
    <descriptorRefs>
      <descriptorRef>jar-with-dependencies</descriptorRef>
    </descriptorRefs>
    <archive>
      <manifest>
        <mainClass>edu.usc.ir.geo.gazetteer.GeoNameResolver</mainClass>
      </manifest>
    </archive>
  </configuration>
  <executions>
    <execution>
      <id>make-assembly</id>
      <phase>package</phase>
      <goals>
        <goal>single</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

### 3. Remove or comment out `animal-sniffer-maven-plugin` (it causes build errors)

```xml
<!-- <plugin>
  <groupId>org.codehaus.mojo</groupId>
  <artifactId>animal-sniffer-maven-plugin</artifactId>
  ...
</plugin> -->
```

---

## 🧪 Build the Project

```bash
mvn clean package
```

Expected output:

```
[INFO] BUILD SUCCESS
```

Fat JAR will be located at:

```
target/lucene-geo-gazetteer-0.3-SNAPSHOT-jar-with-dependencies.jar
```

---

## 🚀 Run the CLI App

```bash
java -jar target/lucene-geo-gazetteer-0.3-SNAPSHOT-jar-with-dependencies.jar --help
```

Expected output:

```
usage: lucene-geo-gazetteer
  -b,--build <gazetteer file>
  -i,--index <directoryPath>
  -s,--search <location>
  -server,--server
  ...
```

---

## 🧱 Next Steps

- Use `--build` to create your Lucene index from GeoNames
- Use `--server` to launch the REST API
- Use `--search` or `--search-reverse` for CLI-based lookups

---

## 🧾 Python Integration Example

You can run geolocation queries directly from Python:

```python
import subprocess

def search_location(index_dir, location_query):
    cmd = [
        "java",
        "-jar",
        "target/lucene-geo-gazetteer-0.3-SNAPSHOT-jar-with-dependencies.jar",
        "--index", index_dir,
        "--search", location_query,
        "--json"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return None

# Example usage
if __name__ == "__main__":
    index_path = "indexDir"  # path to built Lucene index
    search_location(index_path, "Waverly Hills Sanatorium, KY")
```

This script integrates seamlessly with the JAR to automate geocoding from a Python environment.

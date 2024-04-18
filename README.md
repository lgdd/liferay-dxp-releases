# Liferay Releases

Mirror all Liferay Portal/DXP Tomcat bundles found in [releases.json](https://releases.liferay.com/releases.json) as GitHub releases in this repository.

## Usage

Sometimes `releases-cdn.liferay.com` is slow or unresponsive which has an impact in Liferay workspaces when running the `initBundle` command with Gradle or `bundle-support:init` with Maven.

With this mirroring, you can now use URLs from the [releases section](https://github.com/lgdd/liferay-releases/releases) as a fallback for downloading the bundle by editing the `gradle.properties`. For example:

```properties
liferay.workspace.product=dxp-7.3-ga1
liferay.workspace.bundle.url=https://github.com/lgdd/liferay-releases/releases/download/dxp-7.3.10/liferay-dxp-tomcat-7.3.10-ga1-20200930160533946.tar.gz
```

> [!NOTE]  
> Releases are not sorted in a chronological order. Make sure to use the search bar to find the edition and version you're looking for.
# Liferay DXP Releases

Mirror all Liferay DXP Tomcat bundles found in [releases.json](https://raw.githubusercontent.com/lgdd/liferay-product-info/main/releases.json) as GitHub releases in this repository.

## Usage

Sometimes `releases-cdn.liferay.com` is slow or unresponsive which has an impact in Liferay workspaces when running the `initBundle` command with Gradle or `bundle-support:init` with Maven.

With this mirroring, you can now use URLs from the [releases section](https://github.com/lgdd/liferay-dxp-releases/releases) as a fallback for downloading the bundle by editing the `gradle.properties`. For example:

```properties
liferay.workspace.product=dxp-2024.q1.5
liferay.workspace.bundle.url=https://github.com/lgdd/liferay-dxp-releases/releases/download/dxp-2024.q1.5/liferay-dxp-tomcat-2024.q1.5-1712566347.tar.gz
```

For Liferay Portal (CE), you can refer to the official GitHub repository: https://github.com/liferay/liferay-portal/releases

> [!NOTE]
> Releases are not sorted in a chronological order. Make sure to use the search bar to find the edition and version you're looking for.

> [!WARNING]
> Releases found in the JSON file might not be available as a release in this repository. The script currently uses a 10 seconds timeout for each release URL found. The timeouts found at the time of the GitHub action execution are reported [here](timeout.md).
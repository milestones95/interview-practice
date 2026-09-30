# 08/24/2026

# Problem: Package Version Index

# You’re building an internal package registry used by thousands of engineers.

# Each published package version has:

# packageName
# versionNumber — an integer that increases over time
# publishedAt
# isDeprecated

# The system needs to support:

# publish(packageName, versionNumber) — Add a new version.
# deprecate(packageName, versionNumber) — Mark a specific version as deprecated.
# latest(packageName) — Return the highest non-deprecated version.
# closest(packageName, targetVersion) — Return the non-deprecated version whose version number is closest to targetVersion.
# versionsBetween(packageName, low, high) — Return all non-deprecated versions between low and high, inclusive, in ascending order. 

from datetime import datetime

# this is for individual version. Each version belongs to a package
class VersionNode:
    def __init__(self, version, publishedAt, key):
        self.left = None
        self.right = None
        self.key = key
        self.version = version
        self.publishedAt = publishedAt
        self.isDeprecated = False

# a package can contain multiple versions
class Package:

    def __init__(self, name):
        self.root = None
        self.name = name
        self.version_id_to_version = {} # need a way to access the specific version node in the tree


# a package list contains one or more packages. For example, it can contain react, typescript, and openai packages. And each of those packages will have versions
class PackageList:

    def __init__(self):
        self.count = 0 # count the num of packages
        self.package_id_to_package = {} # we need a direct way to access a specific package 


    
    def publish(self, version, package_name):

        # add a package name that hasn't been seen
        if package_name not in self.package_id_to_package:


            # create new package
            package = Package(package_name)

            # add the new package to the list
            self.package_id_to_package[package.name] = package

            # create the new version node
            new_root = self.insert_node(None, version, package_name)
            package.root = new_root
            package.version_id_to_version[version] = new_root # set the new version node in the hash map

            # add the package to the package list

            self.count+=1



        else:
            # find the right package within the list of packages
            package = self.package_id_to_package[package_name]

            # insert the version into the package of versions
            package.root = self.insert_node(package.root, version, package_name)

            # update the package back into the list of packages
            self.package_id_to_package[package_name] = package

        


    def insert_node(self, root, version, name):

        if root is None:
            key = (version, name)
            new_node = VersionNode(version, datetime.now(), key)
            self.package_id_to_package[name].version_id_to_version[key] = new_node
            print("keY : ",key)
            
            return new_node

        if version < root.version:
            root.left = self.insert_node(root.left, version, name)

        else:
            root.right = self.insert_node(root.right, version, name)

        
        return root


    def deprecate(self, package_name, v):

        # get the package first
        package = self.package_id_to_package[package_name]
        key = v, package_name

        # get the version from the package
        version_node = package.version_id_to_version[key]
        print("version: ", version_node.key)
        # deprecate the package
        version_node.isDeprecated = True
        # update the package with the updated version
        package.version_id_to_version[key] = version_node

        # update the list of packages
        self.package_id_to_package[package_name] = package


    def latest(self, package_name):

        package = self.package_id_to_package[package_name]
        latest_version = self.search_latest(package.root, None)

        return latest_version.version


    def search_latest(self, root, potential_latest):

        if root is None:
            return None

        if not root.isDeprecated:
            potential_latest = root


        found = self.search_latest(root.right, potential_latest)

        if found:
            return found

        return potential_latest

    def closest(self, version, name):

        package = self.package_id_to_package[name]

        closest_node = self.search_closest(version, package.root)

        return closest_node.version

    def search_closest(self, version, root):

        if root is None:
            return None

        if root.version == version:
            return root

        if version < root.version:
            found = self.search_closest(version, root.left)

        else:
            found = self.search_closest(version, root.right)

        if found:
            found_diff = abs(found.version - version)
            root_diff = abs(root.version - version)

            if found_diff < root_diff:
                return found
            return root

        else:
            return root


    def versions_between(self, package_name, low, high):

        package = self.package_id_to_package[package_name]
        versions_found = []
        self.find_in_range(package.root, low, high, versions_found)

        return versions_found


    def find_in_range(self, root, low, high, versions_in_range):

        if root is None:
            return

        if root.version < low:
            self.find_in_range(root.right, low, high,versions_in_range)
        
        elif root.version > high:
            self.find_in_range(root.left, low, high,versions_in_range)

        else:

            if not root.isDeprecated:
                versions_in_range.append(root.version)
            
            self.find_in_range(root.right, low, high,versions_in_range)
            self.find_in_range(root.left, low, high,versions_in_range)
            


    def get_versions(self, package_name):

        package = self.package_id_to_package[package_name]
        self.traverse(package.root)

    def traverse(self, root):

        if root is None:
            return


        self.traverse(root.left)
        print("version: ", root.key, " deprecated: ", root.isDeprecated)
        self.traverse(root.right)


test = PackageList()
test.publish(1.2, "React")
test.publish(1.4, "React")
test.publish(1.0, "React")
test.publish(1.8, "React")
test.publish(1.1, "openai")
test.publish(1.3, "openai")
test.publish(1.2, "openai")
test.publish(4.2, "openai")





test.get_versions("React")
test.deprecate("React", 1.4)
test.get_versions("React")

latest_version = test.latest("openai")

print("latest v: ", latest_version)

closest = test.closest(1.9, "openai")
# items = test.package_id_to_package.items()

print("closest: ", closest)

print("-------------------")

between = test.versions_between("React",1, 1.5)

print("between: ", between)

# i got stuck breaking down the classes well enough the first time. second time around i did it in 1hr and 5 mins
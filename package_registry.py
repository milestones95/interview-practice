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

class PackageVersion:

    def __init__(self, id, version):
        self.left = None
        self.right = None
        self.id = id
        self.version = version
        self.isDeprecated = False


class PackageTree:

    def __init__(self, package_name, id):
        self.root = None


class PackageContainer:

    def __init__(self):
        self.count = 0
        # self.tree = PackageTree()
        self.id_to_package_version = {}


class PackageOwners:

    def __init__(self):
        self.count = 0
        self.id_to_package_container = {}

    
    def publish(self, packageName, version):
        id = (packageName, version)

        self.root = self.insert_node(id, version, self.root)


    def insert_node(self, id, packageName, version, root):

        if root is None:
            new_package =  Package(id, version)
            self.id_to_package[id] = new_package
            return new_package

        if version < root.version:
            root.left = self.insert_node(id, version, root.left)

        else:
            root.right = self.insert_node(id, version, root.right)

        return root

    def deprecate(self, packageName, version):

        key = (packageName, version)

        self.id_to_package[key].isDeprecated = True


    def latest(self):
        
        latest_version = self.search_latest(self.root, None)

        return latest_version.id


#                   8
#               /          \
#              3            27
#             /  \         /.  \
#            1.    6      21    34  

    def search_latest(self, root, possible_latest):
        if root is None:
            return None

        if not root.isDeprecated:
            possible_latest = root

        found = self.search_latest(root.right, possible_latest)

        if found:
            return found
        
        return possible_latest

    def traverse(self, root):

        if root is None:
            return

        self.traverse(root.left)
        print("package: ", root.id, " deprecated status: ", root.isDeprecated)
        self.traverse(root.right)


    # def closest(self, root):


    # def find_closest(self, root, )



owners = PackageOwners
    


# tree = PackageContainer()
test = PackageOwners()
test.publish("openai",1.1)
test.publish("openai",1.2)
test.publish("openai",1.3)
test.publish("openai",1.6)

test.traverse(test.root)
test.deprecate("openai",1.2)
test.deprecate("openai",1.6)

test.traverse(test.root)
latest = test.latest()

print("latest: ", latest)


# finished insert, deprecate and latest version by 23 min mark
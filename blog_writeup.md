# AWS Inventory: A Tool for Mapping AWS Resources

# Overview

AWS Inventory is a tool that scans an AWS account looking for [AWS resources](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#resource). There are constantly new services being added to AWS and existing ones are being expanded upon with new features. This ecosystem allows users to piece together many different services to form a customized cloud experience. Creating this customizability at scale comes with a manageability cost. It quickly becomes difficult to audit an AWS account for the different resources being used. Auditing is not only important for billing purposes, but also for security. Dormant and unknown resources are more prone to security configuration weaknesses because they tend to be out of sync with current security policy. Additionally, resources with unexpected dependencies pose availability, access control, and authorization issues.

# Related Projects

There are existing tools that perform similar functionality. AWS provides one called [AWS Config](https://aws.amazon.com/config/). It is "a service that enables you to assess, audit, and evaluate the configurations of your AWS resources". However, it has limited service support and focuses on monitoring for changes in an account. Similarly, there are non-AWS tools that focus on account changes of predefined services like, [Security Monkey](https://github.com/Netflix/security_monkey) and [Edda](https://github.com/Netflix/edda/). [Skew](https://github.com/scopely-devops/skew) is a tool that allows [ARN](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)-based querying for resources in predefined services across an account.

# How it Works

The tool has two components: a Python script to pull data from an AWS account and a single page webapp to view the data as a collapsible tree. Filtering can be done on AWS services, regions, and operations. A text search is also featured.

AWS Inventory uses the low-level AWS SDK for Python called [botocore](https://github.com/boto/botocore) to locally discover [AWS services](https://botocore.readthedocs.io/en/latest/reference/index.html) and what [regions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) they run in. Because of this dependency on a standard interface, the tool does NOT need updating from upstream changes to AWS services. The changes are pulled down with regular updates to botocore in the form of service model files. This is how each service is able to be abstracted away for use by all of the different [AWS SDKs](https://aws.amazon.com/tools/#sdk).

Once the services have been discovered, certain operations within each service are invoked and the responses recorded. Since operations follow a naming convention, those that look like they would enumerate resources are the ones chosen for invocation. The responses are stored in a deeply nested JSON object and dumped to a file.

Finally, the JSON file is consumed by a local [React](https://reactjs.org/) [single-page app](https://en.wikipedia.org/wiki/Single-page_application) where the data can visualized and searched.

# Installation

There is a small GUI for displaying progress which uses the standard Python *Tkinter* module. However, the underlying native library code for Tcl/Tk may need extra steps to install. Then,

`pip install -r requirements.txt`

## Windows

Use the Python installer to install Tkinter/Tcl/Tk.

## Linux

Use your OS package manager:

### Ubuntu / Debian

`sudo apt-get install python-tk`

# Getting Started

You can run the Python script without any parameters. It will search for your AWS credentials in your shell environment, instance metadata, config file, then credentials file. You can also provide a CSV file containing your credentials on the commandline. You will want a user that has permissions like the AWS managed policy *ViewOnlyAccess*. If you are feeling lucky, you could just pipe the output of the tool to a JSON parser like *jq*.

The tool could take a long time (dozens of minutes) to complete if no restrictions are placed on which operations to invoke for each service across each region. Filtering by service and region can be done on the commandline while filtering by service operation can be done via configuration file. A [pre-configured file](https://github.com/nccgroup/aws-inventory/blob/master/operation_blacklist.conf) was created and checked into the source code repository. It will be used by default. 

Aside from the commandline output, you can view the results locally in the webapp. No web server needed. Just open the [HTML file](https://github.com/nccgroup/aws-inventory/blob/master/gui/dist/index.html) in a browser and select the generated JSON file.

The webapp uses [jsTree](https://www.jstree.com/) to display the data in a hierarchical, tree-like structure. There is also a search feature.

## Examples

- Run with defaults.

`$ python aws_inventory.py`

- List AWS services known to *botocore*. This is all done locally by reading service model files.

```
$ python aws_inventory.py --list-svcs
acm
apigateway
application-autoscaling
appstream
autoscaling
batch
budgets
clouddirectory
cloudformation
cloudfront
.
.
.
```

- List service operations known to *botocore*. This is all done locally by reading service model files.

```
$ python aws_inventory.py --list-operations
[shield]
DescribeSubscription
ListAttacks
ListProtections

[datapipeline]
ListPipelines

[firehose]
ListDeliveryStreams
.
.
.
[glacier]
# NONE

[stepfunctions]
ListActivities
ListStateMachines

Total operations to invoke: 4045
```

- Print what operations would be invoked for a service. This is all done locally.

`$ python aws_inventory.py --debug --dry-run`

# Screenshots

![invoking apis on commandline](screenshots/invoking%20apis%20on%20commandline.png)



![data in browser](screenshots/data%20in%20browser.png)

# Roadmap

This tool aims to be a starting point for DevOps, auditors, IT, developers, and incident responders to successfully audit their AWS resources. This current phase of the tool gathers the raw account data and simply displays it as a collapsible tree. The following is a list of ideas for the next phase of AWS Inventory:

* Reduce time in data fetching by ignoring known low utility service operations
* Improve search
  * Query language that understands service semantics (e.g., search on "ec2 instance with default security group") or JSON queries (e.g., [JMESPath](http://jmespath.org/))
  * Search from a select tree node
* Move Python code to webapp
* Compare resources between accounts
* Provide a better user interface allowing the user to see more data at once and allowing them to intuitively sift through all of it.

# Open Source

You can find the source code hosted at https://github.com/nccgroup/aws-inventory. If you are interested in learning more about the AWS ecosystem, checkout this [Awesome List](https://github.com/donnemartin/awesome-aws).
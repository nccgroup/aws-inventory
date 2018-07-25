# Introduction

This is a tool that tries to discover all [AWS resources](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#resource) created in an account. AWS has many products (a.k.a. services) with new ones constantly being added and existing ones expanded with new features. The ecosystem allows users to piece together many different services to form a customized cloud experience. The ability to instantly spin up services at scale comes with a manageability cost. It can quickly become difficult to audit an AWS account for the resources being used. It is not only important for billing purposes, but also for security. Dormant resources and unknown resources are more prone to security configuration weaknesses. Additionally, resources with unexpected dependencies pose availability, access control, and authorization issues.

It uses [botocore](https://github.com/boto/botocore) to discover [AWS services](https://botocore.readthedocs.io/en/latest/reference/index.html) and what [regions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) they run in. It is also used in invoking the service APIs. The APIs that are invoked are those which should list or describe resources. The results can be printed to stdout in JSON format. They can also be written across several files:

* Raw responses from API endpoints can be written to a file specified on the commandline. The file format is [Python pickle](https://docs.python.org/2/library/pickle.html).
* Exceptions raised during tool execution can be written to a file specified on the commandline. The file format is [Python pickle](https://docs.python.org/2/library/pickle.html).
* gui/aws_inventory_data-&lt;environment_name&gt;.json - JSON format. Parsed responses structured for input to the GUI.

# Installation

First, install Python2.7.

There is a small GUI for displaying progress which uses the standard Python *Tkinter* module. However, the underlying native library code for Tcl/Tk may need extra steps to install. Then,

`pip install -r requirements.txt`

## Windows

Use the Python installer to install Tkinter/Tcl/Tk.

## Linux

Use your OS package manager:

### Ubuntu / Debian

`sudo apt-get install python-tk`

# Usage

You can run the script without any parameters. It will search for your AWS creds in your shell environment, instance metadata, config file, then credentials file. You can also provide a CSV file, containing your creds, on the commandline. You will want a user that has permissions like the AWS managed policy [ViewOnlyAccess](arn:aws:iam::aws:policy/job-function/ViewOnlyAccess). If you are feeling lucky, you could just pipe the output of the tool to a JSON parser like *jq*.

The tool could take a long time (dozens of minutes) to complete if no restrictions are placed on which operations to invoke for each service across each region. Filtering by service and region can be done on the commandline while filtering by service operation can be done via configuration file. A [pre-configured file](operation_blacklist.conf) was created and checked into the repository. It will be used by default. 

Aside from the commandline output, you can view the results locally in a [React](https://reactjs.org/) [single-page app](https://en.wikipedia.org/wiki/Single-page_application). No web server needed. Just open the [HTML file](gui/dist/index.html) in a browser and select the generated JSON file when prompted.  

The app uses [jsTree](https://www.jstree.com/) to display the data in a hierarchical, tree-like structure. There is also a search feature.

**NOTE:** When invoking APIs, those that raise an exception are not used again regardless of region. Known causes of exceptions are:

* required API parameter not specified in service model (or the tool is not properly reading model?)
* insufficient authorization for the selected credentials
* network error

## Examples

* Run with defaults.

`$ python aws_inventory.py`

* List AWS services known to *botocore*. This is all done locally by reading service model files.

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

* Print what APIs would be called for a service. This is all done locally.

`$ python aws_inventory.py --debug --dry-run`

# Screenshots

![invoking apis on commandline](screenshots/invoking%20apis%20on%20commandline.png)



![data in browser](screenshots/data%20in%20browser.png)

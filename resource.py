from __future__ import unicode_literals

import uuid

LIST_FUNCS = {
	"microsoft.AnalysisServices/servers": "listGatewayStatus",
	"microsoft.AppConfiguration/configurationStores": "ListKeys",
	"microsoft.Automation/automationAccounts": "listKeys",
	"microsoft.Batch/batchAccounts": "listkeys",
	"microsoft.BatchAI/workspaces/experiments/jobs": "listoutputfiles",
	"microsoft.Blockchain/blockchainMembers": "listApiKeys",
	"microsoft.Blockchain/blockchainMembers/transactionNodes": "listApiKeys",
	"microsoft.Cache/redis": "listKeys",
	"microsoft.CognitiveServices/accounts": "listKeys",
	"microsoft.ContainerRegistry/registries": ["listBuildSourceUploadUrl", "listCredentials", "listUsages"],
	"microsoft.ContainerRegistry/registries/webhooks": "listEvents",
	"microsoft.ContainerRegistry/registries/runs": "listLogSasUrl",
	"microsoft.ContainerRegistry/registries/tasks": "listDetails",
	"microsoft.ContainerService/managedClusters": ["listClusterAdminCredential", "listClusterUserCredential"],
	"microsoft.ContainerService/managedClusters/accessProfiles": "listCredential",
	"microsoft.DataBox/jobs": "listCredentials",
	"microsoft.DataFactory/datafactories/gateways": "listauthkeys",
	"microsoft.DataFactory/factories/integrationruntimes": "listauthkeys",
	"microsoft.DataLakeAnalytics/accounts/storageAccounts/Containers": "listSasTokens",
	"microsoft.DataShare/accounts/shares": "listSynchronizations",
	"microsoft.DataShare/accounts/shareSubscriptions": ["listSourceShareSynchronizationSettings", "listSynchronizationDetails", "listSynchronizations"],
	"microsoft.Devices/iotHubs": "listkeys",
	"microsoft.Devices/iotHubs/iotHubKeys": "listkeys",
	"microsoft.Devices/provisioningServices/keys": "listkeys",
	"microsoft.Devices/provisioningServices": "listkeys",
	"microsoft.DevTestLab/labs": "ListVhds",
	"microsoft.DevTestLab/labs/schedules": "ListApplicable",
	"microsoft.DevTestLab/labs/users/serviceFabrics": "ListApplicableSchedules",
	"microsoft.DevTestLab/labs/virtualMachines": "ListApplicableSchedules",
	"microsoft.DocumentDB/databaseAccounts": ["listConnectionStrings", "listKeys"],
	"microsoft.DomainRegistration": "listDomainRecommendations",
	"microsoft.DomainRegistration/topLevelDomains": "listAgreements",
	"microsoft.EventGrid/domains": "listKeys",
	"microsoft.EventGrid/topics": "listKeys",
	"microsoft.EventHub/namespaces/authorizationRules": "listkeys",
	"microsoft.EventHub/namespaces/disasterRecoveryConfigs/authorizationRules": "listkeys",
	"microsoft.EventHub/namespaces/eventhubs/authorizationRules": "listkeys",
	"microsoft.ImportExport/jobs": "listBitLockerKeys",
	"microsoft.Kusto/Clusters/Databases": "ListPrincipals",
	"microsoft.LabServices/users": ["ListEnvironments", "ListLabs"],
	"microsoft.Logic/integrationAccounts/agreements": "listContentCallbackUrl",
	"microsoft.Logic/integrationAccounts/assemblies": "listContentCallbackUrl",
	"microsoft.Logic/integrationAccounts": ["listCallbackUrl", "listKeyVaultKeys"],
	"microsoft.Logic/integrationAccounts/maps": "listContentCallbackUrl",
	"microsoft.Logic/integrationAccounts/partners": "listContentCallbackUrl",
	"microsoft.Logic/integrationAccounts/schemas": "listContentCallbackUrl",
	"microsoft.Logic/workflows": ["listCallbackUrl", "listSwagger"],
	"microsoft.Logic/workflows/runs/actions": "listExpressionTraces",
	"microsoft.Logic/workflows/runs/actions/repetitions": "listExpressionTraces",
	"microsoft.Logic/workflows/triggers": "listCallbackUrl",
	"microsoft.Logic/workflows/versions/triggers": "listCallbackUrl",
	"microsoft.MachineLearning/webServices": "listkeys",
	"microsoft.MachineLearning/Workspaces": "listworkspacekeys",
	"microsoft.MachineLearningServices/workspaces/computes": ["listKeys", "listNodes"],
	"microsoft.MachineLearningServices/workspaces": "listKeys",
	"microsoft.Maps/accounts": "listKeys",
	"microsoft.Media/mediaservices/assets": ["listContainerSas", "listStreamingLocators"],
	"microsoft.Media/mediaservices/streamingLocators": ["listContentKeys", "listPaths"],
	"microsoft.Network/applicationSecurityGroups": "listIpConfigurations",
	"microsoft.NotificationHubs/Namespaces/authorizationRules": "listkeys",
	"microsoft.NotificationHubs/Namespaces/NotificationHubs/authorizationRules": "listkeys",
	"microsoft.OperationalInsights/workspaces": "listKeys",
	"microsoft.PolicyInsights/remediations": "listDeployments",
	"microsoft.Relay/namespaces/authorizationRules": "listkeys",
	"microsoft.Relay/namespaces/disasterRecoveryConfigs/authorizationRules": "listkeys",
	"microsoft.Relay/namespaces/HybridConnections/authorizationRules": "listkeys",
	"microsoft.Relay/namespaces/WcfRelays/authorizationRules": "listkeys",
	"microsoft.Search/searchServices": ["listAdminKeys", "listQueryKeys"],
	"microsoft.ServiceBus/namespaces/authorizationRules": "listkeys",
	"microsoft.ServiceBus/namespaces/disasterRecoveryConfigs/authorizationRules": "listkeys",
	"microsoft.ServiceBus/namespaces/queues/authorizationRules": "listkeys",
	"microsoft.ServiceBus/namespaces/topics/authorizationRules": "listkeys",
	"microsoft.SignalRService/SignalR": "listkeys",
	"microsoft.Storage/storageAccounts": ["listAccountSas", "listkeys", "listServiceSas"],
	"microsoft.StorSimple/managers/devices": ["listFailoverSets", "listFailoverTargets"],
	"microsoft.StorSimple/managers": ["listActivationKey", "listPublicEncryptionKey"],
	"microsoft.Web/connectionGateways": "ListStatus",
	"microsoft.web/connections": "listconsentlinks",
	"microsoft.Web/customApis": "listWsdlInterfaces",
	"microsoft.web/locations": "listwsdlinterfaces",
	"microsoft.web/apimanagementaccounts/apis/connections": ["listconnectionkeys", "listsecrets"],
	"microsoft.web/sites/backups": "list",
	"microsoft.Web/sites/config": "list",
	"microsoft.web/sites/functions": ["listkeys", "listsecrets"],
	"microsoft.web/sites/hybridconnectionnamespaces/relays": "listkeys",
	"microsoft.web/sites": "listsyncfunctiontriggerstatus",
	"microsoft.web/sites/slots/functions": "listsecrets",
	"microsoft.web/sites/slots/backups": "list",
	"microsoft.Web/sites/slots/config": "list",
}
PROVIDERS = [
	"microsoft.datashare",
	"microsoft.azureactivedirectory",
	"microsoft.netapp",
	"microsoft.media",
	"microsoft.guestconfiguration",
	"microsoft.blueprint",
	"microsoft.kusto",
	"microsoft.sqlvirtualmachine",
	"microsoft.appconfiguration",
	"microsoft.databoxedge",
	"microsoft.devops",
	"microsoft.saas",
	"microsoft.healthcareapis",
	"microsoft.changeanalysis",
	"microsoft.securityinsights",
	"microsoft.offazure",
	"microsoft.datamigration",
	"microsoft.authorization",
	"microsoft.classicstorage",
	"microsoft.management",
	"microsoft.datafactory",
	"microsoft.apimanagement",
	"microsoft.classicinfrastructuremigrate",
	"microsoft.botservice",
	"microsoft.domainregistration",
	"microsoft.commerce",
	"microsoft.resourcehealth",
	"microsoft.alertsmanagement",
	"microsoft.datalakestore",
	"microsoft.managedidentity",
	"microsoft.notificationhubs",
	"microsoft.datalakeanalytics",
	"microsoft.eventhub",
	"microsoft.advisor",
	"microsoft.relay",
	"microsoft.keyvault",
	"microsoft.signalrservice",
	"microsoft.devices",
	"microsoft.datacatalog",
	"microsoft.batch",
	"microsoft.analysisservices",
	"microsoft.visualstudio",
	"microsoft.compute",
	"microsoft.security",
	"microsoft.machinelearningservices",
	"microsoft.servicebus",
	"microsoft.databricks",
	"microsoft.storage",
	"microsoft.documentdb",
	"microsoft.containerinstance",
	"microsoft.scheduler",
	"microsoft.search",
	"microsoft.insights",
	"microsoft.storagesync",
	"microsoft.dbforpostgresql",
	"microsoft.powerbi",
	"microsoft.capacity",
	"microsoft.powerbidedicated",
	"microsoft.logic",
	"microsoft.classiccompute",
	"microsoft.hdinsight",
	"microsoft.cdn",
	"microsoft.operationsmanagement",
	"microsoft.policyinsights",
	"microsoft.portal",
	"microsoft.containerservice",
	"microsoft.dbformysql",
	"microsoft.eventgrid",
	"microsoft.machinelearning",
	"microsoft.cognitiveservices",
	"microsoft.cache",
	"microsoft.containerregistry",
	"microsoft.devtestlab",
	"microsoft.streamanalytics",
	"microsoft.devspaces",
	"microsoft.web",
	"microsoft.sql",
	"sendgrid.email",
	"microsoft.network",
	"microsoft.classicnetwork",
	"microsoft.servicefabric",
	"microsoft.operationalinsights",
	"microsoft.recoveryservices",
	"microsoft.automation",
	"microsoft.dbformariadb",
	"microsoft.migrate",
	"84codes.cloudamqp",
	"conexlink.mycloudit",
	"crypteron.datasecurity",
	"livearena.broadcast",
	"mailjet.email",
	"microsoft.aad",
	"microsoft.addons",
	"microsoft.adhybridhealthservice",
	"microsoft.appplatform",
	"microsoft.attestation",
	"microsoft.azuredata",
	"microsoft.azurestack",
	"microsoft.batchai",
	"microsoft.billing",
	"microsoft.bingmaps",
	"microsoft.blockchain",
	"microsoft.certificateregistration",
	"microsoft.classicsubscription",
	"microsoft.consumption",
	"microsoft.costmanagement",
	"microsoft.costmanagementexports",
	"microsoft.customerlockbox",
	"microsoft.customproviders",
	"microsoft.databox",
	"microsoft.deploymentmanager",
	"microsoft.desktopvirtualization",
	"microsoft.enterpriseknowledgegraph",
	"microsoft.experimentation",
	"microsoft.features",
	"microsoft.hanaonazure",
	"microsoft.hardwaresecuritymodules",
	"microsoft.hybridcompute",
	"microsoft.hybriddata",
	"microsoft.hydra",
	"microsoft.importexport",
	"microsoft.iotcentral",
	"microsoft.iotspaces",
	"microsoft.kubernetes",
	"microsoft.labservices",
	"microsoft.maintenance",
	"microsoft.managedservices",
	"microsoft.maps",
	"microsoft.marketplace",
	"microsoft.marketplaceapps",
	"microsoft.marketplaceordering",
	"microsoft.mixedreality",
	"microsoft.objectstore",
	"microsoft.peering",
	"microsoft.projectbabylon",
	"microsoft.providerhub",
	"microsoft.resourcegraph",
	"microsoft.resources",
	"microsoft.serialconsole",
	"microsoft.servicefabricmesh",
	"microsoft.services",
	"microsoft.softwareplan",
	"microsoft.solutions",
	"microsoft.storagecache",
	"microsoft.storsimple",
	"microsoft.subscription",
	"microsoft.support",
	"microsoft.timeseriesinsights",
	"microsoft.token",
	"microsoft.virtualmachineimages",
	"microsoft.vmwarecloudsimple",
	"microsoft.vnfmanager",
	"microsoft.vsonline",
	"microsoft.windowsesu",
	"microsoft.windowsiot",
	"microsoft.workloadmonitor",
	"myget.packagemanagement",
	"paraleap.cloudmonix",
	"pokitdok.platform",
	"ravenhq.db",
	"raygun.crashreporting",
	"sparkpost.basic",
	"stackify.retrace",
	"u2uconsult.theidentityhub",
]

# def _resourcegroup_(*items):
# 	return "[resourcegroup]"

# def _subscription_(*items):
# 	return "[subscription]"

def _reference_(*items, **kwargs):
	arm = kwargs.get("arm")
	return arm.get_resource_by_id(*items)

def _resourceid_(*items, **kwargs):
	pivot = 0
	for index, item in enumerate(items):
		if item and item.lower().split("/")[0] in PROVIDERS:
			pivot = index
			break

	subscription_id = kwargs.get("subscription_id")
	resource_group_name = kwargs.get("resource_group_name")
	resource_type = items[pivot]
	resource_name = []
	for name in items[pivot + 1:]:
		resource_name.append(name.strip("/") if name else "")
	resource_name = "/".join(resource_name)

	for item in items[:pivot]:
		if _validate_uuid(item):
			subscription_id = item
		else:
			resource_group_name = item

	return "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_type}/{resource_name}".format(
		subscription_id=subscription_id,
		resource_group_name=resource_group_name,
		resource_type=resource_type,
		resource_name=resource_name
	)

def _listkeys_(*items):
	return {"primaryKey": "primaryKey", "secondaryKey": "secondaryKey", "keys": [{"value": "primaryKey"}, {"value": "secondaryKey"}]}

def _providers_(*items):
	return "[providers]"

def _extensionresourceid_(*items):
	return "[extensionresourceid]"

def _subscriptionresourceid_(*items, **kwargs):
	pivot = 0
	for index, item in enumerate(items):
		if item.lower() in PROVIDERS:
			pivot = index
			break

	subscription_id = kwargs.get("subscription_id")
	resource_type = items[pivot]
	resource_name = []
	for name in items[pivot + 1:]:
		resource_name.append(name)
	resource_name = "/".join(resource_name)
	if pivot > 0:
		subscription_id = items[0]
	return "/subscriptions/{subscription_id}/providers/{resource_type}/{resource_name}".format(
		subscription_id=subscription_id,
		resource_type=resource_type,
		resource_name=resource_name
	)

def _tenantresourceid_(*items):
	resource_type = items[0]
	resource_name = []
	for name in items[1:]:
		resource_name.append(name)
	resource_name = "/".join(resource_name)
	return "/providers/{resource_type}/{resource_name}".format(
		resource_type=resource_type,
		resource_name=resource_name
	)


def _validate_uuid(data):
	try:
		uuid_obj = uuid.UUID(data, version=4)
	except ValueError:
		return False
	return str(uuid_obj) == data

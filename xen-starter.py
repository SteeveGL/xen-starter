#! /usr/bin/python

import logging, os, re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

tagAutostart = "Auto start"

logger.info('')
logger.info('*****************************************')
logger.info(' Created by : SteeveGL.DEV')
logger.info(' Contact : steevegl.dev@gmail.com')
logger.info(' Source : http://github.com/steevegldev/xen-starter')
logger.info(' 2015-09-26')
logger.info('*****************************************')
logger.info('')
logger.info('Script started.')
logger.info('')

def _isAutostart(uuid):
        global tagAutostart
        vmTags = os.popen("xe vm-param-get uuid=%s param-name=tags" % uuid).read().split(",")
        #logger.debug("vmTags=%s" % vmTags)
        #logger.debug("tagAutostart in vmTags=%s" % (tagAutostart in vmTags))
        if tagAutostart in vmTags:
                return True

        return False

def VMList():
        logger.info('Loading VMs list...')

        vmlist = os.popen("xe vm-list is-control-domain=false").read().split("\n\n\n")
        #logger.debug("vmlist=%s" % vmlist)
        vmArray = []
        for vm in vmlist:
                if vm:
                        #logger.debug("vm=%s" % vm)
                        arg = re.findall('\s?(\w+)\s\(.+:\s(.+)?', vm)
                        #logger.debug("arg=%s" % arg)
                        vmUUID = arg[0][1]
                        vmLabel = arg[1][1]
                        logger.info('VM found: %s' % vmLabel)
                        # #logger.debug(vmUUID)
                        isAutostart = _isAutostart(vmUUID)
                        logger.info('Auto start: %s' % isAutostart)
                        if isAutostart:
                                vmArray.append(arg)
                                logger.info('Added to the starting queue.')
                                # if len(vmArray) == 0:
                                        # vmArray = arg
                                # else:
                                        # vmArray.append(arg)
                        else:
                                logger.info('Skipped')
                        logger.info('')

        #logger.debug("vmArray=%s" % vmArray)
        return vmArray

#logger.debug("VMList()=%s" % VMList())
#print VMList()

VMTaggedAutostart = VMList()
logger.info('Starting VMs...')
for vm in VMTaggedAutostart:
        logger.info('%s is %s' % (vm[1][1], vm[2][1]))
        if "running" in vm:
                logger.info('Starting' % vm[1][1])
                os.popen("xe vm-start uuid=%s" % vm[0][1])
                logger.info('%s is now %s' % (vm[1][1], vm[2][1]))
        else:
                logger.info('%s skipped.' % vm[1][1])

#!/usr/bin/python
'''
This script can do both metric collection and alerting on queues, exchanges, or messages in a given queue
'''
import sys
from pyrabbit.api import Client
import optparse

parser = optparse.OptionParser()

parser.add_option('-u', '--user',
  help  = 'user to bind as',
  dest  = 'rmqUser',
  metavar = 'RMQUSER')

parser.add_option('-p', '--pass',
  help  = 'pass for user to bind as',
  dest  = 'rmqPass',
  metavar = 'RMQPASS')

parser.add_option('-m', '--msgqueue',
  help  = 'queue name to get message count for',
  dest  = 'rmqQueue',
  metavar = 'RMQQUEUENAME')

parser.add_option('-q', '--queuecount',
  help  = 'monitor number of queues',
  dest  = 'numQueues',
  default = False)

parser.add_option('-e', '--exchangecount',
  help  = 'monitor number of exchanges',
  dest  = 'numExchanges',
  default = False)

parser.add_option('-c', '--crit',
  help  = 'crit at this number of messages',
  dest  = 'crit',
  metavar = 'CRIT')

parser.add_option('-v', '--vhost',
  help  = 'vhost to use',
  dest  = 'rmqVhost',
  metavar = 'VHOST')

parser.add_option('-w', '--warn',
  help  = 'warn at this number of messages',
  dest  = 'warn',
  metavar = 'WARN')

parser.add_option('-P', '--port',
  help  = 'rmq port',
  dest  = 'rmqPort',
  metavar = 'RMQPORT')

parser.add_option('-H', '--host',
  help  = 'rmq host',
  dest  = 'rmqHost',
  metavar = 'RMQHOST')

parser.add_option('-s', '--scheme',
  help = 'Graphite string to prepend for metrics',
  dest = 'scheme',
  metavar = 'SCHEME')

(options, args) = parser.parse_args()

cl = Client('%s:%s' % (options.rmqHost, options.rmqPort), options.rmqUser, options.rmqPass, timeout=15) 

if options.numExchanges:
  numExchanges = cl.get_overview()['object_totals']['exchanges']
  if options.scheme:
    print options.scheme+'.rmqQueueStats.ExchangeCount.'+str(numExchanges)
  else:
    if int(numExchanges) > int(options.warn) and int(numExchanges) > int(options.crit):
      print 'Number of exchanges CRITICAL - %s' % (numExchanges)
      sys.exit(2)
    if int(numExchanges) > int(options.warn) and int(numExchanges) < int(options.crit):
      print 'Number of exchanges WARNING - %s' % (numExchanges)
      sys.exit(1)

if options.numQueues:
  numQueues = cl.get_overview()['object_totals']['queues']
  if options.scheme:
    print options.scheme+'.rmqQueueStats.QueueCount.'+str(numQueues)
  else:
    if int(numQueues) > int(options.warn) and int(numQueues) > int(options.crit):
      print 'Number of queues CRITICAL - %s' % (numQueues)
      sys.exit(2)
    if int(numQueues) > int(options.warn) and int(numQueues) < int(options.crit):
      print 'Number of queues WARN - %s' % (numQueues)
      sys.exit(1)


if options.rmqQueue and options.rmqVhost and options.rmqQueue:
  numMessagesInQueue = cl.get_messages(options.rmqVhost, options.rmqQueue)[0]['message_count']
  if options.scheme:
    print options.scheme+'.rmqQueueStats.'+options.rmqQueue+'.'+str(numMessagesInQueue)
  else:
    if int(numMessagesInQueue) > int(options.warn) and int(numMessagesInQueue) > int(options.crit):
      print 'Messages in queue %s CRITICAL - %s' % (options.rmqQueue, numMessagesInQueue)
      sys.exit(2)
    if int(numMessagesInQueue) > int(options.warn) and int(numMessagesInQueue) < int(options.crit):
      print 'Messages in queue %s WARN - %s' % (options.rmqQueue, numMessagesInQueue)
      sys.exit(1)

/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50513
Source Host           : localhost:3306
Source Database       : web_data

Target Server Type    : MYSQL
Target Server Version : 50513
File Encoding         : 65001

Date: 2017-09-02 18:45:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for performance
-- ----------------------------
DROP TABLE IF EXISTS `performance`;
CREATE TABLE `performance` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `navigation` int(11) DEFAULT NULL,
  `url` varchar(255) NOT NULL,
  `score` int(11) DEFAULT NULL,
  `flag` int(11) DEFAULT NULL,
  `navigationStart` bigint(20) DEFAULT NULL,
  `unloadEventStart` bigint(20) DEFAULT NULL,
  `unloadEventEnd` bigint(20) DEFAULT NULL,
  `redirectStart` bigint(20) DEFAULT NULL,
  `redirectEnd` bigint(20) DEFAULT NULL,
  `fetchStart` bigint(20) DEFAULT NULL,
  `domainLookupStart` bigint(20) DEFAULT NULL,
  `domainLookupEnd` bigint(20) DEFAULT NULL,
  `connectStart` bigint(20) DEFAULT NULL,
  `secureConnectionStart` bigint(20) DEFAULT NULL,
  `connectEnd` bigint(20) DEFAULT NULL,
  `requestStart` bigint(20) DEFAULT NULL,
  `responseStart` bigint(20) DEFAULT NULL,
  `responseEnd` bigint(20) DEFAULT NULL,
  `domLoading` bigint(20) DEFAULT NULL,
  `domInteractive` bigint(20) DEFAULT NULL,
  `domContentLoadedEventStart` bigint(20) DEFAULT NULL,
  `domContentLoadedEventEnd` bigint(20) DEFAULT NULL,
  `domComplete` bigint(20) DEFAULT NULL,
  `loadEventStart` bigint(20) DEFAULT NULL,
  `loadEventEnd` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for resource
-- ----------------------------
DROP TABLE IF EXISTS `resource`;
CREATE TABLE `resource` (
  `test_id` int(10) unsigned NOT NULL,
  `resource_id` int(10) unsigned NOT NULL,
  `name` varchar(4096) DEFAULT NULL,
  `entryType` varchar(255) DEFAULT NULL,
  `startTime` decimal(32,10) DEFAULT NULL,
  `duration` decimal(32,10) DEFAULT NULL,
  `initiatorType` varchar(255) DEFAULT NULL,
  `redirectStart` decimal(32,10) DEFAULT NULL,
  `redirectEnd` decimal(32,10) DEFAULT NULL,
  `fetchStart` decimal(32,10) DEFAULT NULL,
  `domainLookupStart` decimal(32,10) DEFAULT NULL,
  `domainLookupEnd` decimal(32,10) DEFAULT NULL,
  `connectStart` decimal(32,10) DEFAULT NULL,
  `connectEnd` decimal(32,10) DEFAULT NULL,
  `secureConnectionStart` decimal(32,10) DEFAULT NULL,
  `requestStart` decimal(32,10) DEFAULT NULL,
  `responseStart` decimal(32,10) DEFAULT NULL,
  `responseEnd` decimal(32,10) DEFAULT NULL,
  `transferSize` int(11) DEFAULT NULL,
  `nextHopProtocol` varchar(255) DEFAULT NULL,
  `workerStart` decimal(32,10) DEFAULT NULL,
  `encodedBodySize` int(11) DEFAULT NULL,
  `decodedBodySize` int(11) DEFAULT NULL,
  PRIMARY KEY (`test_id`,`resource_id`),
  CONSTRAINT `ref` FOREIGN KEY (`test_id`) REFERENCES `performance` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `gender` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `education` int(11) DEFAULT NULL,
  `occupation` int(11) DEFAULT NULL,
  `netage` int(11) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  `isp` varchar(1023) DEFAULT NULL,
  `country` varchar(1023) DEFAULT NULL,
  `area` varchar(1023) DEFAULT NULL,
  `region` varchar(1023) DEFAULT NULL,
  `city` varchar(1023) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;

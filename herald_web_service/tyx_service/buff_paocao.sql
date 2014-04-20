/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50532
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50532
File Encoding         : 65001

Date: 2014-04-26 12:25:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `buff_paocao`
-- ----------------------------
DROP TABLE IF EXISTS `buff_paocao`;
CREATE TABLE `buff_paocao` (
  `ykt` int(11) NOT NULL,
  `num` int(11) NOT NULL,
  `query_date` int(11) NOT NULL,
  PRIMARY KEY (`ykt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of buff_paocao
-- ----------------------------
INSERT INTO `buff_paocao` VALUES ('0', '1', '1398486235');
INSERT INTO `buff_paocao` VALUES ('213120498', '30', '1398486208');

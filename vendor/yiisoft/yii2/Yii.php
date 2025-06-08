<?php
namespace yii;
class Yii {
    public static function createObject($type, array $params = []) {
        return new $type(...$params);
    }
}

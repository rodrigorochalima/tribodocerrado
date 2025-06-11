<?php
namespace app\controllers;
use yii\web\Controller;

class SiteController extends Controller
{
    public function actionIndex()
    {
        return $this->render('index');
    }
    
    public function actionError()
    {
        return 'Erro na aplicação';
    }
}


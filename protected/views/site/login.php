<?php
$this->pageTitle=Yii::app()->name . ' - Login';
?>

<div style="text-align: center; margin-top: 50px;">
    <img src="/images/logo.png" alt="Logo Tribo do Cerrado" style="width: 180px; margin-bottom: 20px;">
    <h1 style="font-family: Arial, sans-serif;">Bem-vindo à Tribo do Cerrado</h1>
    <p style="font-size: 1.2em;">A Tribo do Cerrado recebe todas as tribos do motociclismo. Sejam bem-vindos.</p>

    <div style="width: 300px; margin: 30px auto; text-align: left;">
        <?php $form=$this->beginWidget('CActiveForm', array(
            'id'=>'login-form',
            'enableClientValidation'=>true,
            'clientOptions'=>array(
                'validateOnSubmit'=>true,
            ),
        )); ?>

        <div class="row">
            <?php echo $form->labelEx($model,'username'); ?>
            <?php echo $form->textField($model,'username', array('class'=>'form-control')); ?>
            <?php echo $form->error($model,'username'); ?>
        </div>

        <div class="row">
            <?php echo $form->labelEx($model,'password'); ?>
            <?php echo $form->passwordField($model,'password', array('class'=>'form-control')); ?>
            <?php echo $form->error($model,'password'); ?>
        </div>

        <div class="row rememberMe">
            <?php echo $form->checkBox($model,'rememberMe'); ?>
            <?php echo $form->label($model,'rememberMe'); ?>
        </div>

        <div class="row buttons" style="margin-top: 15px;">
            <?php echo CHtml::submitButton('Entrar', array('class'=>'btn btn-primary')); ?>
        </div>

        <?php $this->endWidget(); ?>
    </div>
</div>

<html>
    <head>
        <title>Página Principal - Curso DS</title>
    </head>
    <body>
        <h1>Calculadora</h1>
       <form action = "index.php" method="post">

       Digite o primeiro valor: <input type = text name=valor1> <br>
       Digite o segundo valor: <input type = text name=valor2> <br>

       <input type = submit value="OK">

       <?php
              

              $valor1 = $_POST['valor1'];
              $valor2 = $_POST['valor2'];
              $soma = $valor1+$valor2;

              echo"<p>";
              echo "A soma do valor 1 com o do valor 2 é de: $soma";
      ?>

    
    </body>
</html>
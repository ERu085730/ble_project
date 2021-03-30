<?php 

	require_once 'dbConnect.php';
	
	//an array to display response
	$response = array();
	
	//if it is an api call 
	//that means a get parameter named api call is set in the URL 
	//and with this parameter we are concluding that it is an api call

	if(isset($_GET['apicall'])){
		
		switch($_GET['apicall']){
			
			case 'all':
				//checking the parameters required are available or not 
				if(isTheseParametersAvailable(array('command'))){
					//getting the values
					$command= $_POST['command'];
                    $row=array();
                    //$rep=array();
					//checking if the user is already exist with this username or email
					//as the email and username should be unique for every user 
					$stmt = $conn->prepare("$command");
					$stmt->execute();
					//$stmt->bind_result();
                    //$stmt->fetch();
                    $rep =$stmt->get_result();
                    //echo $num_of_rows = $rep->num_rows;

                    if ($cnt=substr("$command",0,1)=="s"){
                        $stmt->fetch();
                        while ($row[] = $rep->fetch_assoc()) {}
                        $stmt->close();
                        $response['response']=$row;

                    }
                    else{
                        $response['message'] = '成功';
                   	}
                	}else{
					$response['error'] = true; 
					$response['message'] = 'required parameters are not available'; 
				}
				
			break; 
		}

	}else{
		//if it is not api call 
		//pushing appropriate values to response array 
		$response['error'] = true; 
		$response['message'] = 'Invalid API Call';
	}
	
	//displaying the response in json structure 
	echo json_encode($response);
	
	//function validating all the paramters are available
	//we will pass the required parameters to this function 
	function isTheseParametersAvailable($params){
		
		//traversing through all the parameters 
		foreach($params as $param){
			//if the paramter is not available
			if(!isset($_POST[$param])){
				//return false 
				return false; 
			}
		}
		//return true if every param is available 
		return true; 
	}
?>
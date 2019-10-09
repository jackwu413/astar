import java.util.Scanner;
import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

class Node{
	public int x;
	public int y;
	public int g;
	public int h;
	public int f;
	public Node parent;
	public boolean blocked;
	public boolean visited; 

	public Node(int x, int y, boolean blocked){
		this.x = x;
		this.y = y;
		this.blocked = blocked;
	}
}


class astar {
	public static void main(String args[]){

		Scanner input = new Scanner(System.in);
		int mazeNum;
		char algo;


		while(true){
			System.out.println("Enter a maze number between 1 and 50 (inclusive).");
			mazeNum = input.nextInt();
			if(mazeNum > 50 || mazeNum < 1){
				System.out.println("Improper input. Try again.");
			} else {
				break;
			}
		}

		while(true){
			System.out.println("Enter F for FORWARD, B for BACKWARD, or A for ADAPTIVE");
			algo = input.next().charAt(0);
			if(algo != 'f' && algo != 'b' && algo != 'a'){
				System.out.println("Improper input. Try again.");
			} else {
				break;
			}
		}


		Node[][] array = loadMaze(mazeNum);
		execute(array, algo);


	}

	public static Node[][] loadMaze(int mazeNum){
		Node[][] array = new Node[5][5];
		String cwd = System.getProperty("user.dir");
		String dir = cwd + "/mazes/";
		File folder = new File(dir);
		File[] files = folder.listFiles();
		for(File file: files){
			if(file.toString().indexOf("maze" + Integer.toString(mazeNum) + ".txt") != -1){
				try {
					BufferedReader br = new BufferedReader(new FileReader(file));
    				String line;
    				int i = 0;
    				while ((line = br.readLine()) != null) {
       					Node[] subArray = new Node[line.length()];
       					int j = 0;
       					while(j < line.length()){
       						char x = line.charAt(j);
       						if(x == 'X'){
       							subArray[j] = new Node(i, j, true);
       						} else {
       							subArray[j] = new Node(i, j, false);
       						}
       						//System.out.println('(' + Integer.toString(subArray[j].x) + ',' + Integer.toString(subArray[j].y) + ')' );
       						j++;
       					}
       					array[i] = subArray;
       					i++;
    				}
				} catch (FileNotFoundException e){
					System.out.println("File Not Found");
				} catch (IOException e){
					System.out.print("IO Exception");
				}

			}
		}
		return array;
	}

	public static void execute(Node[][] array, char algo){
		if(algo == 'f'){
			System.out.println("Executing Repeated Forward A*");

			//Initialize openList and closeList

			ArrayList<Node> closeList = new ArrayList<Node>();

			Node curr = array[4][2];
			Node goal = array[array.length-1][array[0].length-1];

			while(curr != goal){
				ArrayList<Node> neighbors = getNeighbors(curr, array);
				System.out.println(neighbors.size());
				return;
			}
		}
	}

	public static ArrayList<Node> getNeighbors(Node curr, Node[][] array){
		ArrayList<Node> neighbors = new ArrayList<Node>();
	    if(curr.x == 0 && curr.y == 0){                             
	        neighbors.add(array[curr.x][curr.y+1]);
	        neighbors.add(array[curr.x+1][curr.y]);
	        return neighbors;
	    }else if (curr.x == 0 && curr.y == array.length-1){               
	        neighbors.add(array[curr.x+1][curr.y]);
	        neighbors.add(array[curr.x][curr.y-1]);
	        return neighbors;
	    }else if (curr.x == array[0].length-1 && curr.y == 0){            
	        neighbors.add(array[curr.x-1][curr.y]);
	        neighbors.add(array[curr.x][curr.y+1]);
	        return neighbors;
	    }else if (curr.x == array[0].length-1 && curr.y == array.length-1){ 
	        neighbors.add(array[curr.x][curr.y-1]);
	        neighbors.add(array[curr.x-1][curr.y]);
	        return neighbors;
	    }else if(curr.x == 0){                                         
	        neighbors.add(array[curr.x+1][curr.y]);
	        neighbors.add(array[curr.x][curr.y+1]);
	        neighbors.add(array[curr.x][curr.y-1]);
	        return neighbors;
	    }else if(curr.x == array.length-1){                                
	        neighbors.add(array[curr.x-1][curr.y]);
	        neighbors.add(array[curr.x][curr.y+1]);
	        neighbors.add(array[curr.x][curr.y-1]);
	        return neighbors;
	    }else if(curr.y == 0){                                          
	        neighbors.add(array[curr.x][curr.y+1]);
	        neighbors.add(array[curr.x+1][curr.y]);
	        neighbors.add(array[curr.x-1][curr.y]);
	        return neighbors;
	    }else if(curr.y == array[0].length-1){                             
	        neighbors.add(array[curr.x][curr.y-1]);
	        neighbors.add(array[curr.x+1][curr.y]);
	        neighbors.add(array[curr.x-1][curr.y]);
	        return neighbors;
	    }else{                                                        
	        neighbors.add(array[curr.x+1][curr.y]);
	        neighbors.add(array[curr.x-1][curr.y]);
	        neighbors.add(array[curr.x][curr.y+1]);
	        neighbors.add(array[curr.x][curr.y-1]);
	        return neighbors;
		}
	}
}





































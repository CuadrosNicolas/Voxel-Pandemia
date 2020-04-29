package main

import (
	"fmt"
	"sync"
	"sort"
	"encoding/json"
	"io/ioutil"
	"os"
	"time"
	"flag"
)

func getEmpty3DArray(size int) [][][]int {
	out := [][][]int{}
	for i := 0; i < size; i++ {
		slice := [][]int{}
		for j := 0; j < size; j++ {
			line := []int{}
			for k := 0; k < size; k++ {
				line = append(line,0)
			}	
			slice = append(slice,line)
		}
		out = append(out,slice)
	}
	return out
}

//Return how the viruses progress depending on the first infected position
func getProgression(x int, y int, z int, size int) []int {

	validPlace := func(x int, y int, z int) bool {
		return x >= 0 && x < size && y >= 0 && y < size && z >= 0 && z < size
	}
	testCasesOf := func(i int, j int, k int) []coordinates {
		return []coordinates{
			coordinates{i+1,j,k},
			coordinates{i-1,j,k},
			coordinates{i,j+1,k},
			coordinates{i,j-1,k},
			coordinates{i,j,k+1},
			coordinates{i,j,k-1},
		}
	}
	day := 1
	addedPerDay := []int{1}
	testCases := []coordinates{coordinates{x,y,z}}
	arr := getEmpty3DArray(size)
	arr[x][y][z] = 1
	for len(testCases) != 0 {
		day += 1

		nextTestCases := []coordinates{}
		contaminated := 0
		for _,testCase := range(testCases) {
			for _,coord := range(testCasesOf(testCase.x,testCase.y,testCase.z)) {
				if validPlace(coord.x,coord.y,coord.z)  && arr[coord.x][coord.y][coord.z] == 0 {
					contaminated += 1
					arr[coord.x][coord.y][coord.z] = 1
					nextTestCases = append(nextTestCases, coord)
				}
			}	
		}
		if contaminated > 0 {
			addedPerDay = append(addedPerDay,contaminated)
		}

		testCases = nextTestCases

	}
	return addedPerDay
}

//Coordinates holder
type coordinates struct {
	x int
	y int
	z int
}
//Return all possible combination of distinct coordinates giving distinct sequences
func getTranslation(size int) []coordinates {
	out := []coordinates{}
	
	for i:=0.0;i<float64(size)/2.0;i++ {
		for j:=0.0;j<i+1;j++ {
			for k:=0.0;k<j+1;k++ {
				out = append(out, coordinates{int(i),int(j),int(k)})
			}
		}
	}

	return out
}

//Virus progression holder
type result struct {
	sequences []int
	coordinate coordinates
	index int
}

//Format result informations
func (res result) infos() string{
	seqString := "["
	for i,c := range(res.sequences) {
		seqString += fmt.Sprintf("%d",c)
		if i < len(res.sequences) -1 {
			seqString += ", "
		} else {
			seqString += "]"
		}
	}
	translationString := fmt.Sprintf("[%d, %d, %d]",res.coordinate.x,res.coordinate.y,res.coordinate.z)
	return fmt.Sprintf("Sequence : %s\nTranslation : %s",seqString,translationString)
}

//String padding from : https://play.golang.org/p/zciRZvD0Gr
func PadRight(str, pad string, lenght int) string {
	for {
		str += pad
		if len(str) > lenght {
			return str[0:lenght]
		}
	}
}

//Print results in a fancy table
func (res result) fancyPrint(size int) {
	title := "| Jour | Total | Contamination | Pourcentage de contamination |"
	fmt.Println(res.infos())
	line := PadRight("","-",len(title))
	fmt.Println(line)
	fmt.Println(title)
	fmt.Println(line)
	count := 0
	percChar := "%"
	for i,v := range(res.sequences) {
		count += v
		countThisDay := v
		percentage := (float64(count)/(float64(size)*float64(size)*float64(size)))*100.0
		pr := fmt.Sprintf("| %s | %s | %s | %s |",
				PadRight(fmt.Sprintf("%d",i+1)," ",len("Jour")),
				PadRight(fmt.Sprintf("%d",count)," ",len("Total")),
				PadRight(fmt.Sprintf("%d",countThisDay)," ",len("Contamination")),
				PadRight(fmt.Sprintf("%3.2f%s",percentage,percChar)," ",len("Pourcentage de contamination")))
		fmt.Println(pr)
		fmt.Println(line)
	}
}

type ConfFile struct {
	CubeSize 	    int `json:"size"`
	LimitOne 	bool  `json:"limit"`
}

func main() {
	verbose := flag.Bool("v",false,"Print all results")
	flag.Parse()
	conf := ConfFile{}
	jsonConf, _ := os.Open("conf.json")
	byteValue, _ := ioutil.ReadAll(jsonConf)
	json.Unmarshal(byteValue,&conf)
 	//Size of the cube
	size := conf.CubeSize
	//Get all possible translations
	translations := getTranslation(size)
	//Defines wait groups and channel for parrallel computing
	wg := sync.WaitGroup{}
	ch := make(chan result, len(translations))
	//Start the timer
	start := time.Now()
	//For each translation compute the result and send it to the channel
	for i,v := range(translations) {
		wg.Add(1)
		go func(v coordinates, wg *sync.WaitGroup,index int) {
			ch <- result{getProgression(v.x,v.y,v.z,size),v,index}
			wg.Done()
		}(v, &wg,i)
	}
	wg.Wait()
	close(ch)

	elapsed := time.Since(start)
	if  *verbose {
		//Sort the result in the order of their position in the translations array
		ordered := []result{}
		for res := range ch {
			ordered = append(ordered,res)
		}
		sort.SliceStable(ordered, func(i,j int) bool {
			return ordered[i].index < ordered[j].index
		})
		//Print all results
		for _,res := range(ordered) {
			res.fancyPrint(size)
		}
	}
	fmt.Printf("Total groups : %d\n",len(translations))
	//Show the elapsed time
	fmt.Printf("Elapsed time : %s\n",elapsed)
}
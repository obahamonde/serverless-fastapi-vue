  const z = ref( 0 );
  
  const add = ( a, b ) => {
      z.value = a + b;
  };
  
  const minus = ( a, b ) => {
      z.value = a - b;
  };
  
  const multiply = ( a, b ) => {
      z.value = a * b;
  };
  
  const divide = ( a, b ) => {
      z.value = a / b;
  };
  
  const power = ( a, b ) => {
      z.value = a ** b;
  };
  
  const root = ( a, b ) => {
      z.value = a ** ( 1 / b );
  };
  
  const app = createApp( {
      setup() {
          const x = ref( 0 );
          const y = ref( 0 );
          const operator = ref( "+" );
          const operators = ["+", "-", "x", "/", "^", "√"];
          const state = reactive( {
              x,
              y,
              z,
              operator,
          } );
          watchEffect( () => {
              state.x = Number( state.x );
              state.y = Number( state.y );
              switch ( state.operator ) {
                  case "+":
                      add( state.x, state.y );
                      break;
                  case "-":
                      minus( state.x, state.y );
                      break;
                  case "x":
                      multiply( state.x, state.y );
                      break;
                  case "/":
                      divide( state.x, state.y );
                      break;
                  case "^":
                      power( state.x, state.y );
                      break;
                  case "√":
                      root( state.x, state.y );
                      break;
                  default:
                      break;
              }
          } );
          return {
              state,
              operators,
          };
      },
      template: `
        <section class="p-16 flex flex-col items-center bg-gray-500 h-screen w-screen">
        <h1 class="flex flex-col items-center
        outline-none text-4xl font-bold text-gray-700 text-center
        
        ">
          <div class="flex flex-row items-center">
            <input type="number" v-model="state.x"   class="text-center w-32 rounded"  /><strong
            class="text-center w-32 rounded"
            >{{state.operator}}</strong>  <input type="number" v-model="state.y"
            class="text-center w-32 rounded"
            /><strong class=" mx-4 ">=</strong><h2 
            class="text-center  bg-gray-300 text-black font-extrabold px-16 py-2 w-64 rounded-lg"
            >{{state.z}}</h2></h1>
            <div class='grid grid-cols-2 gap-4 p-12'>        
              <button v-for="operator in operators" 
             @click="state.operator = operator"
              class="bg-gray-300 text-black font-extrabold px-16 py-2 mx-2 my-2 w-96 rounded-lg shadow-lg"
              >{{operator}}</button> 
          </div>
        </div>
      </section>
      `,
  } );
  
  app.mount( "#app" );

  app.unmount()

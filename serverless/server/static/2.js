const TodoApp = defineComponent({
  name: 'TodoApp',
  setup() {
    const todos = reactive([
      { id: 1, text: 'Learn Vue 3', done: false },
      { id: 2, text: 'Learn FastAPI', done: false },
      { id: 3, text: 'Learn Git', done: false },
    ])
    const newTodo = ref('')
    const addTodo = () => {
      if (newTodo.value.trim()) {
        todos.push({
          id: todos.length + 1,
          text: newTodo.value,
          done: false,
        })
        newTodo.value = ''
      }
    }
    const removeTodo = (todo) => {
      const index = todos.indexOf(todo)
      todos.splice(index, 1)
    }
    const toggleTodo = (todo) => {
      todo.done = !todo.done
    }
    const clearCompleted = () => {
      todos.splice(0, todos.length, ...todos.filter((todo) => !todo.done))
    }
    const remaining = computed(() => todos.filter((todo) => !todo.done).length)
    const allDone = computed({
      get: () => todos.length && todos.every((todo) => todo.done),
      set: (value) => todos.forEach((todo) => (todo.done = value)),
    })
    const save = async()=>{
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(todos),
      })
      if (response.ok) {
        alert('Saved!')
      }
    }



    return {
      todos,
      newTodo,
      addTodo,
      removeTodo,
      toggleTodo,
      clearCompleted,
      remaining,
      allDone,
      save
    }
  },
  template: `

   
      <div class="flex flex-col items-center gap-4 p-16">
        <h1 class="text-2xl">Tasks</h1>
        <div class="flex flex-row items-center">
          <span class="px-2 py-1">{{ remaining }} task(s) pending</span>
          <button
            class="bg-blue-500 text-white rounded px-2 py-1 ml-2"
            @click="allDone = true"
          >
            Mark All
          </button>
          <button
            class="bg-blue-500 text-white rounded px-2 py-1 ml-2"
            @click="allDone = false"
          >
            Unmark All
          </button>
          <button
            class="bg-cyan-500 text-white rounded px-2 py-1 ml-2"
            @click="clearCompleted"
          >
            Clear Completed
          </button>
          <button
            class="bg-green-500 text-white rounded px-2 py-1 ml-2"
            @click="save"
          >
            Save
          </button>
        </div>
        <div class="flex flex-col items-center gap-4">
          <input
            type="text"
            class="border border-gray-300 rounded px-2 py-1"
            v-model="newTodo"
            @keyup.enter="addTodo"
          />
          <button
            class="bg-blue-500 text-white rounded px-2 py-1 ml-2"
            @click="addTodo"
          >
            Add
          </button>
        </div>
        
        <div class="flex flex-col items-center">
          <div
            v-for="todo in todos"
            :key="todo.id"
            class="flex flex-row items-center m-4"
          >
            <input
              type="checkbox"
              class="border border-gray-300 rounded px-2 py-1"
              :checked="todo.done"
              @change="toggleTodo(todo)"
            />
            <span
              class="px-2 py-1"
              :class="{ 'line-through': todo.done }"
            >{{ todo.text }}</span>
            <button
              class="bg-red-500 text-white rounded px-2 py-1 ml-2"
              @click="removeTodo(todo)"
            >
              Remove
            </button>
          </div>
        </div>
       
      </div>
  `,
})

createApp(TodoApp).mount('#app')

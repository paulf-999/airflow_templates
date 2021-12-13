def test_xcoms(self):
    dag_id = "hello_world_xcoms"
    dag = self.dagbag.get_dag(dag_id)
    push_to_xcoms_task = dag.get_task("push_to_xcoms")
    pull_from_xcoms_task = dag.get_task("pull_from_xcoms")

    execution_date = datetime.now()

    push_to_xcoms_ti = TaskInstance(task=push_to_xcoms_task, execution_date=execution_date)
    context = push_to_xcoms_ti.get_template_context()
    push_to_xcoms_task.execute(context)

    pull_from_xcoms_ti = TaskInstance(task=pull_from_xcoms_task, execution_date=execution_date)

    result = pull_from_xcoms_ti.xcom_pull(key="dummyKey")
    self.assertEqual(result, "dummyValue")

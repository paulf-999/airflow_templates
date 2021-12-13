def push_to_xcoms(*args, **kwargs):
    value = "dummyValue"
    kwargs["ti"].xcom_push(key="dummyKey", value=value)


def pull_from_xcoms(**kwargs):
    ti = kwargs["ti"]
    pulled_value = ti.xcom_pull(key="dummyKey", task_ids="push_to_xcoms")
    print("value=" + str(pulled_value))


push_to_xcoms_task = PythonOperator(task_id="push_to_xcoms", provide_context=True, python_callable=push_to_xcoms, dag=dag)

pull_from_xcoms_task = PythonOperator(task_id="pull_from_xcoms", provide_context=True, python_callable=pull_from_xcoms, dag=dag)

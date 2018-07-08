node {
    def docker_img = "myusername/myproject"
    def gitCommit = ""
    def img_suffix = ""
    dir('src_temp') {
        checkout scm
        gitCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
        img_suffix = "${gitCommit}-${env.BUILD_NUMBER}"
        stage("Setup Infra") {
            sh("docker run --rm -d --name mysql_${img_suffix} -v /data/dockervol/data/mysql/var/lib/mysql:/var/lib/mysql mysql")
        }
        stage("Build") {
            def ver = sh(returnStdout: true, script:  "cat src/VERSION.txt").trim()
            sh "docker build -t='${docker_img}' --target app -f build/Dockerfile ."
            sh "docker build -t='${docker_img}-static' --target static -f build/Dockerfile ."
        }
    }
    stage("Test") {
        try {
            retry(10) {
                sleep 5
                sh("docker run --rm -i \
                    -v '${env.WORKSPACE}/tests/results/':/tmp/tests/results \
                    --link mysql_${img_suffix}:mysql \
                    ${docker_img} python manage.py test")
                junit 'tests/results/*.xml'
            }
        } finally {
            stage("Cleanup") {
                sh("docker stop mysql_${img_suffix}")
            }
        }
    }
    stage("Push Docker"){
        withDockerRegistry([credentialsId: 'registry-creds']) {
            if (env.BRANCH_NAME in ["master", "release-${ver}".toString()]) {
                sh("docker tag ${docker_img} ${docker_img}:${ver}-app")
                sh("docker push ${docker_img}:${ver}-app")
                sh("docker tag ${docker_img}-static ${docker_img}:${ver}-static")
                sh("docker push ${docker_img}:${ver}-static")
            } else {
                sh("docker tag ${docker_img} ${docker_img}:${ver}-${env.BUILD_NUMBER}-app")
                sh("docker push ${docker_img}:${ver}-${env.BUILD_NUMBER}-app")
                sh("docker tag ${docker_img}-static ${docker_img}:${ver}-${env.BUILD_NUMBER}-static")
                sh("docker push ${docker_img}:${ver}-${env.BUILD_NUMBER}-static")
            }
        }
    }
}